Command line tool for converting PDFs to images then running OCR on the image
you can optionally preprocess the image, however this is only recommended if the image is in a bad quality




how to use
----------------------
make sure the working directory has a folder called pdf_in
put PDFs into the pdf_in folder
run main.py in command line
wait for outputted text in text_out
you can also view your processed images in img_out


supported languages
---------------------
English
Russian
Chinese Trad
Chinese Simp

Dependencies
---------------------------
opencv-python
numpy
pillow
pytesseract
pdf2image
poppler

