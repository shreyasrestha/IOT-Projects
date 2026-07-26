import cv2
import pytesseract
import numpy as np
import sys
import time
import smbus  # Direct native I2C control library

try:
    from picamera2 import Picamera2
except ImportError:
    print("Error: picamera2 library not found.")
    sys.exit(1)

# =====================================================================
#                DIRECT SMBUS I2C LCD CONTROL (STANDALONE PROOF)
# =====================================================================
class DirectI2CLCD:
    def __init__(self, address=0x27):
        self.address = address
        self.is_alive = False
        
        self.LCD_CHR = 1  
        self.LCD_CMD = 0  
        self.LINE_1 = 0x80 
        self.LINE_2 = 0xC0 
        self.BACKLIGHT = 0x08  # 0x08 = ON, 0x00 = OFF
        self.ENABLE = 0b00000100 

        try:
            self.bus = smbus.SMBus(1)
            time.sleep(0.1) 
            
            self.raw_write_nibble(0x30, self.LCD_CMD)
            time.sleep(0.005)
            self.raw_write_nibble(0x30, self.LCD_CMD)
            time.sleep(0.001)
            self.raw_write_nibble(0x30, self.LCD_CMD)
            time.sleep(0.001)
            self.raw_write_nibble(0x20, self.LCD_CMD) 
            time.sleep(0.001)
            
            self.write_raw_byte(0x28, self.LCD_CMD) 
            self.write_raw_byte(0x0C, self.LCD_CMD) 
            self.write_raw_byte(0x06, self.LCD_CMD) 
            self.write_raw_byte(0x01, self.LCD_CMD) 
            time.sleep(0.005)
            
            self.is_alive = True
            print(f"-> Hardware I2C LCD connected at: {hex(address)}")
        except Exception:
            print(f"-> Hardware screen missing at {hex(address)}. Terminal output only.")

    def raw_write_nibble(self, val, mode):
        data = mode | (val & 0xF0) | self.BACKLIGHT
        self.bus.write_byte(self.address, data)
        self.toggle_enable_pulse(data)

    def write_raw_byte(self, bits, mode):
        try:
            high_nibble = mode | (bits & 0xF0) | self.BACKLIGHT
            low_nibble = mode | ((bits << 4) & 0xF0) | self.BACKLIGHT

            self.bus.write_byte(self.address, high_nibble)
            self.toggle_enable_pulse(high_nibble)
            
            self.bus.write_byte(self.address, low_nibble)
            self.toggle_enable_pulse(low_nibble)
        except IOError:
            self.is_alive = False

    def toggle_enable_pulse(self, bits):
        time.sleep(0.0001)
        self.bus.write_byte(self.address, (bits | self.ENABLE))
        time.sleep(0.0005)
        self.bus.write_byte(self.address, (bits & ~self.ENABLE))
        time.sleep(0.0001)

    def write_message(self, text, row_line):
        if not self.is_alive: return
        text = text.ljust(16, " ")[:16]
        if row_line == 1:
            self.write_raw_byte(self.LINE_1, self.LCD_CMD)
        elif row_line == 2:
            self.write_raw_byte(self.LINE_2, self.LCD_CMD)
        
        for char in text:
            self.write_raw_byte(ord(char), self.LCD_CHR)

    def clear_screen(self):
        if not self.is_alive: return
        self.write_raw_byte(0x01, self.LCD_CMD)
        time.sleep(0.005)

# =====================================================================
#                            IMAGE LOGIC
# =====================================================================
def preprocess_image(frame):
    """
    Cleans up the image, keeps strokes crisp, and adds a white border
    so Tesseract doesn't panic if text gets close to the edge.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    bordered = cv2.copyMakeBorder(thresh, 30, 30, 30, 30, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    return bordered

# =====================================================================
#                            MAIN RUNNER
# =====================================================================
def main():
    # ⚠️ Double-check your screen address here (usually 0x27 or 0x3F)
    TARGET_ADDRESS = 0x27 
    
    # Init hardware screen layout
    lcd = DirectI2CLCD(address=TARGET_ADDRESS)
    lcd.write_message("Tesseract Camera", 1)
    lcd.write_message("System Ready...", 2)

    print("Initializing Raspberry Pi Camera via Picamera2...")
    picam = Picamera2()
    picam.configure(picam.create_preview_configuration(main={"size": (1280, 720)}))
    picam.start()

    print("\n=== OCR Camera Started Successfully ===")
    print("Instructions:")
    print("1. Position your text so it is fully visible with space around it.")
    print("2. Press [SPACE] to capture and scan.")
    print("3. Press [Q] to quit.\n")

    try:
        while True:
            frame = picam.capture_array()
            cv2.imshow("Camera Preview - Press SPACE to Scan", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                print("Exiting application...")
                lcd.clear_screen()
                lcd.write_message("System Closed", 1)
                break

            elif key == ord(' '):
                print("\n--- Capturing & Processing Image... ---")
                lcd.clear_screen()
                lcd.write_message("Capturing...", 1)
                lcd.write_message("Running AI OCR...", 2)

                cleaned_img = preprocess_image(frame)
                cv2.imshow("Processed Image (What Tesseract Sees)", cleaned_img)
                
                print("Running AI OCR Text Extraction...")
                custom_config = r'--psm 8'
                
                try:
                    extracted_text = pytesseract.image_to_string(cleaned_img, config=custom_config)
                    clean_output = extracted_text.strip()
                    
                    print("\n================ RECOGNIZED TEXT ================")
                    if clean_output:
                        print(clean_output)
                        
                        # --- OUTPUT DATA TO THE I2C SCREEN ---
                        lcd.clear_screen()
                        lcd.write_message(clean_output[:16], 1) # Print first 16 characters on Row 1
                        if len(clean_output) > 16:
                            lcd.write_message(clean_output[16:32], 2) # Print next 16 characters on Row 2
                    else:
                        print("[No text detected - Pull the camera back further!]")
                        lcd.clear_screen()
                        lcd.write_message("No Text Found", 1)
                        lcd.write_message("Adjust Distance", 2)
                    print("=================================================\n")
                    
                except Exception as e:
                    print(f"OCR Error occurred: {e}")
                    lcd.clear_screen()
                    lcd.write_message("OCR Error", 1)

    finally:
        print("Stopping camera hardware safely...")
        picam.stop()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main() 