
# import the necessary packages
import os
import re
import shutil
from pathlib import Path

import pytesseract
from typing import List
from pdf2image import convert_from_path
from PIL import Image



def grayscale_image(image) -> Image:
    # convert the pillow image to grayscale
    return image.convert("L")


def pdf_to_image(path_pdf: str, img_path: str, output_path: str) -> None:
    # check if in the data folder there are any pdfs
    # if there are, convert them to images
    pdfs = Path(path_pdf).rglob("*.pdf")

    # check if the generator is empty
    for f in pdfs:
        if f is None:
            break

        # new subfolder for each pdf
        Path(os.path.join(img_path, f.stem)).mkdir(parents=True, exist_ok=True)


        images = convert_from_path(f"{f}")
        for i, image in enumerate(images):
            image.save(f"{img_path}/{f.stem}/{f.stem}_{i}.jpg", "JPEG")

        # copy all images in the data folder to the images folder
        images = Path(path_pdf).rglob("*.jpg")
        save_images(images, img_path)
        images = Path(path_pdf).rglob("*.png")
        save_images(images, img_path)
        images = Path(path_pdf).rglob("*.jpeg")
        save_images(images, img_path)

def save_images(image_list, img_path:str):
    for f in image_list:
        # create subfolder for each pdf
        sub_path= os.path.join(img_path, f.stem)
        Path(sub_path).mkdir(parents=True, exist_ok=True)
        shutil.copy(f, sub_path)

def process_text_from_pdf(path_pdf: str, output_path: str) -> None:
    pdfs = Path(path_pdf).rglob("*.pdf")






def ocr(img_path: str, output_path: str) -> None:
    # collect all files in the images folder
    images = Path(img_path).rglob("*.*")
    Path(output_path).mkdir(parents=True, exist_ok=True)

    # iterate over all of the images
    for f in images:
        # load the image as a PIL/Pillow image, apply OCR, and then store the text in a file
        print(f"Processing {f}")
        text = pytesseract.image_to_string(Image.open(f).convert("L"), lang="deu")
        # remove the line breaks if there are more than 2 directly behind each other
        text = re.sub(r'(\n){2,}', '\n', text)
        # write the text to a file
        Path(os.path.join(output_path, f.parents[0].name)).mkdir(parents=True, exist_ok=True)
        with open(f"{output_path}/{f.parents[0].name}/{f.stem}.txt", "w") as file:
            file.write(text)
