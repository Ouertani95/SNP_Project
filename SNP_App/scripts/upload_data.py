from datetime import datetime
from csv import DictReader


def upload_file_locally(f):
    date_time = datetime.now()
    file_name = f"{date_time.strftime('%Y_%m_%d_%X')}_{f.name}"
    with open(f"SNP_App/uploads/{file_name}", 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_name

def has_all_fields(file_name):
    required_fields = ["DISEASE/TRAIT", "PUBMEDID", "JOURNAL", "STUDY", "DATE", "CHR_ID", "CHR_POS", "SNPS"]
    # open file in read mode
    with open(f'SNP_App/uploads/{file_name}', 'r') as read_obj:
        # pass the file object to DictReader() to get the DictReader object
        csv_dict_reader = DictReader(read_obj)
        # get column names from a csv file
        column_names = csv_dict_reader.fieldnames
        for field in required_fields:
            if field not in column_names:
                return False
        return True





