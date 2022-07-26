import cv2 
import argparse
import os
import torch 
import easyocr
import numpy as np 
import datetime as dt 
from project_utils import create_connection

parser = argparse.ArgumentParser()
parser.add_argument('--device', default=0, help="""The serial number of webcam device from which you would like to 
                    perform detection, usually 0 but can be greater than 0 in case multiple devices are attached""")

parser.add_argument('--path', default=None, help='The path of video footage you would like to detect license plate in')
parser.add_argument('--version', default=0, help="""The version of model you would like to use to perform the detections, 
                    -1 for latest, 0 for pre trained, otherwise enter the version number""")
parser.add_argument('--position', default=None, help='The camera position, select from entry or exit')
parser.add_argument('--society', default=None, help='The name of the society in which this project is being used')

args = parser.parse_args()

if args.society is None:
    raise ValueError('Please enter a society name')
if args.position is None:
    raise ValueError('Please enter a camera position')
if args.position.upper() not in ['ENTRY','EXIT']:
    raise ValueError("Please select the camera position from ['ENTRY', 'EXIT']")

query = f"CREATE TABLE IF NOT EXISTS {args.society.upper()} LIKE BASE"
connection = create_connection()
cursor = connection.cursor()
cursor.execute(query)
connection.commit()
connection.close()

runs_path = os.path.join('yolov5', 'runs', 'train')

if args.version == 0:
    path = 'best.pt'
elif args.version == -1:
    latest_run = os.listdir(runs_path)[-1]
    path = os.path.join(runs_path, latest_run, 'weights', 'best.pt')
else:
    latest_run = os.listdir(runs_path)[args.version]
    path = os.path.join(runs_path, latest_run, 'weights', 'best.pt')
      
model = torch.hub.load('ultralytics/yolov5', 'custom', path=path)

source = args.device if args.path is None else args.path
reader = easyocr.Reader(lang_list=['en'])
cap = cv2.VideoCapture(source)
while cap.isOpened():
    ret, frame = cap.read()
    results = model(frame)
    final_img = np.squeeze(results.render())
    try:
        # Getting co ordinates of license plate
        results_df = results.pandas().xyxy[0].loc[0]
        x_min = int(results_df['xmin'])
        x_max = int(results_df['xmax'])
        y_min = int(results_df['ymin'])
        y_max = int(results_df['ymax'])
        # Cropping license plate from image 
        number_plate = frame[y_min:y_max,x_min:x_max]
        # Converting the number plate to grayscale
        number_plate = cv2.cvtColor(number_plate, cv2.COLOR_RGB2GRAY)
        # Binarizing the image 
        _, number_plate = cv2.threshold(number_plate, 128,255, cv2.THRESH_BINARY)
        texts = reader.readtext(number_plate)
        license_plate_no = texts[0][-2] if len(texts) == 1 else ' '.join([text[-2] for text in texts])
        final_img = cv2.putText(final_img, str(license_plate_no), org=(x_min, y_max), 
                                fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, color=(0,255,0), thickness=2)
        query = f"""INSERT INTO {args.society.upper()} (LICENSE_NO, DETECTION_TIMESTAMP, CAMERA_POSITION) VALUES ('{license_plate_no}', 
        '{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%d')}', '{args.position.upper()}')"""
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()
    except:
        pass
    cv2.imshow('Image', final_img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()