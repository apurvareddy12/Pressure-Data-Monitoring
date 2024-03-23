import cv2
import pytesseract
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import time
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
import os
os.chdir(r"C:/Users/Dell/Desktop/SCALES/Pressure")
cap = cv2.VideoCapture(0)

count = 0
counts = []
pressures = []

file_created = False
csv_filename = ""

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()
    
def append_to_csv(file_name,date, current_time, value):
    
    with open(file_name, mode='a', newline='',encoding='utf-8-sig') as file:
        
        writer = csv.writer(file)
        writer.writerow([date,current_time,value])

def create_csv_file():
    
    timestamp =datetime.now().strftime("%m-%d-%Y-%H-%M")
    filename = f"Data/Pressure_{timestamp}.csv"
    print(f"Creating CSV file: {filename}")
    with open(filename, 'w', newline='',encoding='utf-8-sig') as file:
        
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Date','Time','Pressure (hPa)'])

        return filename

def real_time_pressure_monitoring(pressure):
   
   global count
   count = count + 1
   counts.append(count)
   pressures.append(pressure)
   
   plt.plot(counts, pressures, linestyle='-', color='g',marker = 'o')
   plt.title('Real Time Pressure Monitoring')
   plt.xlabel('Counts')
   plt.ylabel('Pressure')
   
   plt.show()

def ocr(crop):
    
   global file_created, csv_filename
    
   text = pytesseract.image_to_string(crop)
   text = text.replace(', ', '.')
   text = str(text.split(" ")[0])

   if '+' not in text:
       return
   if text and text[-1] == '8':
       text = text[:-1] + '0'

   try:
       text1 = float(text)
   except ValueError:
       print(f"Error converting text to float: '{text}'")
       return
   
   print(text)

   current_date = datetime.now().strftime('%d-%m-%Y')
   current_time = datetime.now().strftime('%H:%M:%S')
   
   if not file_created:
        csv_filename = create_csv_file()
        file_created = True
   append_to_csv(csv_filename,current_date,current_time,text)
    
   real_time_pressure_monitoring(text1)
       
def crop_image(frame):
    
    crop = frame[195:239,266:390]
    cv2.imwrite(f'C:/Users/Dell/Desktop/SCALES/Pressure/Frames/frame_{frame_count}.png',crop)
    ocr(crop)

try:
    frame_count = 0  
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture frame.")
            break
        
        crop_image(frame)
        frame_count += 1
        time.sleep(8)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
