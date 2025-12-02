import pytesseract
from PIL import Image
import os

def OCR_(output_folder="./text_out", input_folder="./img_out"):
    what_lang = input("What language is your document in?:\n"
    "(1) English \n"
    "(2) Russian \n"
    "(3) Chinese (Simplified)\n"
    "(4) Chinese (Traditional)\n"
    "(5) Arabic \n"
    "(6) All (not recommended for single language documents)\n")

    if what_lang == "1":
        lang="eng"
    elif what_lang == "2":
        lang="rus"
    elif what_lang == "3":
        lang="chi_sim+eng"
    elif what_lang == "4":
        lang="chi_tra+eng"
    elif what_lang == "5":
        lang="ara+eng"
    elif what_lang == "6":
        lang="ara+eng+chi_tra+chi_sim+rus"
    else:
        print("Please input a number")
        return

    os.makedirs(output_folder, exist_ok=True)

    for folder in os.listdir(input_folder):
        pdf_img_folder = os.path.join(input_folder, folder)
        if not os.path.isdir(pdf_img_folder):
            continue
        if not folder.endswith("_images"):
            continue

        pdf_stem = folder[:-len("_images")]
        pdf_text_folder = os.path.join(output_folder, f"{pdf_stem}_text")
        os.makedirs(pdf_text_folder, exist_ok=True)

        images = [f for f in os.listdir(pdf_img_folder)
                  if f.lower().endswith((".jpg",".jpeg",".png",".tif",".tiff",".bmp"))]
        images.sort()

        for img_name in images:
            img_path = os.path.join(pdf_img_folder, img_name)
            base, _ = os.path.splitext(img_name)
            txt_name = f"{base}.txt"
            txt_path = os.path.join(pdf_text_folder, txt_name)

            print(f"OCR'ing {img_name} please wait")
            im = Image.open(img_path)
            text = pytesseract.image_to_string(im, lang=lang, config="--psm 6")

            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"OCR complete: {img_name}")
