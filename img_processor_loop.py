import cv2
import os
from img_processor import OCRProcessor

def preprocess_loop (input_folder = "img_out"):
    for dirpath, dirnames, filenames in os.walk(input_folder):
        for file in filenames:
            path = os.path.join(dirpath, file)
            print (f"Preprocessing {file}")

            processor = OCRProcessor(path)
    
            processor.deskew()
            processor.bw()
            processor.gray()
            processor.noise_removal()
            processor.thicken()
            processor.remove_borders()
            cv2.imwrite(path,processor.img)

            print("Preprocessing complete.\n")