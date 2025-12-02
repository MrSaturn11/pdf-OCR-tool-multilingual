from pdf2image import convert_from_path
import os

def pdf2images(pdf_folder= "./pdf_in",
               output_folder="img_out",
               poppler_path=r"C:\\Program Files\\poppler-25.11.0\\Library\\bin"
               ):
    os.makedirs(pdf_folder, exist_ok=True)

    os.makedirs(output_folder, exist_ok=True)
    
    for pdf in os.listdir(pdf_folder):
        
        if pdf.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, pdf)
            pdf_root = os.path.splitext(pdf)[0]
            pdf_img_folder = os.path.join(output_folder, f"{pdf_root}_images")
            os.makedirs(pdf_img_folder, exist_ok=True)
            print(f"converting: {pdf} to image(s), please wait")
            pages = convert_from_path(pdf_path, poppler_path=poppler_path, dpi = 400)
            
            for page_num, page in enumerate(pages):
                page_name = f"{pdf_root}_page_{page_num}.jpg"
                out_path = os.path.join(pdf_img_folder, page_name)
                page.save(out_path,'JPEG')
    print("Complete")