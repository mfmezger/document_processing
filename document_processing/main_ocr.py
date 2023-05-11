from pathlib import Path
from loguru import logger
from dotenv import dotenv_values
from document_processing.ocr.ocr import pdf_to_image, ocr
from document_processing.extraction.extraction import generate_prompt, send_request, extract_information_from_table
from document_processing.validation.validate import validate_ouputs

img_path = "data/images"
path_pdf = "data/input"
output_path = "data/output"

config = dotenv_values(".env")


def main():

    

    # start by converting all pdfs to images
    pdf_to_image(path_pdf=path_pdf, img_path=img_path, output_path=output_path)

    # then process the images
    ocr(img_path=img_path, output_path=output_path)

    # iterate over the output folder and extract the text
    for f in Path(output_path).rglob("*.txt"):
        prompt = generate_prompt(prompt_name="extract_sender.txt", text=f.read_text())

        # send the request to the api
        response = send_request(text=prompt, token=config["AA_Token"])

        logger.info(f"Response: {response}")

        # extract the information from the table using the regex
        matches = extract_information_from_table(model_output=response)

        # validate the outputs
        validate_ouputs(outputs=matches,name=f.name)



if __name__ == '__main__':
    main()