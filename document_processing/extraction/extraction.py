"""Extraction of the information in the text with luminous."""
import os
import re

from aleph_alpha_client import Client, CompletionRequest, Prompt
from jinja2 import Template
from loguru import logger

regex = r"\|\w+\|(.*)\|"


def generate_prompt(prompt_name: str, text: str) -> str:
    """Generate the prompt for the luminous api out of a jinja template.

    :param prompt_name: Name of the File with the jinja template
    :type prompt_name: str
    :param text: The text to be inserted into the template
    :type text: str
    :return: The generated prompt
    :rtype: str
    """
    with open(os.path.join("prompts", prompt_name)) as f:
        prompt = Template(f.read())

    # replace the value text with jinja
    # Render the template with your variable
    prompt = prompt.render(text=text)

    # logger.info(f"Generated prompt: {prompt}")
    return prompt


def send_request(text: str, token: str) -> str:
    """Send the request to the luminous api.

    :param text: The prompt to be sent to the api
    :type text: str
    :param token: The token for the luminous api
    :type token: str
    :return: The response from the api
    :rtype: str
    """
    client = Client(token=token)
    request = CompletionRequest(prompt=Prompt.from_text(text), maximum_tokens=256, stop_sequences=["###"])
    response = client.complete(request, model="luminous-supreme")

    return response.completions[0].completion


def extract_information_from_table(model_output: str) -> re.Match:
    """Extract the information from the table using the regex.

    :param model_output: The output from the luminous api
    :type model_output: str
    :return: The matches from the regex
    :rtype: re.Match
    """
    # extract the information from the table using the regex
    matches = re.findall(regex, f"|{model_output}")
    logger.info(matches)

    return matches
