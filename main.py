from img_processor_loop import preprocess_loop
from ocr import OCR_
from PdfToImage import pdf2images

def main():

    ask = input("do you want to preprocess the image? (reccomended for low quality documents) (y/n):").lower()
    pdf2images()

    if ask == "y": 
        preprocess_loop()
        print("Preprocessing finished")
        
    else:
        print("Image not preprocessed")
    
    OCR_()

if __name__ =="__main__":
    main()