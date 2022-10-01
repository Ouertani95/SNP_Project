import pandas as pd
from SNP_App.models import SNP, DiseaseTrait, Reference, Association


def file_upload(file_path: str):
    associations_file = None
    try:
        associations_file = pd.read_csv(file_path, sep="\t")
    except:
        return {"Message": "Error while loading file please check if you used a tsv file."}
    if associations_file is not None:
        for association in associations_file:
            return

