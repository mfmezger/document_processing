import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from loguru import logger
from Levenshtein import distance

def validate_ouputs(outputs:str, name:str):


    # first load the files for the validation
    if name == "privatrechnung-vorlage.txt":
        rechnung = pd.read_csv("solutions/privatrechnung-vorlage.txt", header=None)
    else:
        rechnung = pd.read_csv("solutions/screenshot-nettorechnung-01-lexoffice-rechnungsprogramm.txt", header=None)

    # convert the outputs to a dataframe
    outputs = pd.DataFrame(outputs)

    # convert to numpy array
    rechnung = rechnung.to_numpy()
    outputs = outputs.to_numpy()

    # calculate the metrics
    accuracy = accuracy_score(rechnung, outputs)
    f1 = f1_score(rechnung, outputs, average='macro')
    precision = precision_score(rechnung, outputs, average='macro')
    recall = recall_score(rechnung, outputs, average='macro')

    logger.info(f"Accuracy: {accuracy}")
    logger.info(f"F1: {f1}")
    logger.info(f"Precision: {precision}")
    logger.info(f"Recall: {recall}")


    # loop over the outputs and calculate the levenshtein distance
    for i in range(len(rechnung)):
        logger.info(f"Levenshtein distance: {distance(rechnung[i], outputs[i])}")
    
