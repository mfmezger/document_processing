import os
import re
from jinja2 import Template
from loguru import logger
from aleph_alpha_client import Client,Prompt,CompletionRequest

regex = r"\|\w+\|(.*)\|"


def generate_prompt(prompt_name:str, text:str):
    with open(os.path.join("prompts", prompt_name), "r") as f:
        prompt = Template(f.read())

    # replace the value text with jinja
    # Render the template with your variable
    prompt = prompt.render(text=text)

    # logger.info(f"Generated prompt: {prompt}")
    return prompt


def send_request(text:str, token:str):

    client = Client(token=token)
    request = CompletionRequest(
    prompt=Prompt.from_text(text),
    maximum_tokens=256, stop_sequences=["###"]
    )
    response = client.complete(request, model="luminous-supreme")

    return response.completions[0].completion


def extract_information_from_table(model_output:str):

    # extract the information from the table using the regex
    matches = re.findall(regex, f'|{model_output}')
    logger.info(matches)

    return matches