from datetime import datetime
from csv import DictReader

from SNP_App.models import SNP, Reference, DiseaseTrait, Association
import pandas as pd


class FileUploader:
    REQUIRED_FIELDS = ["PUBMEDID", "JOURNAL", "STUDY", "DATE", "CHR_ID", "CHR_POS", "SNPS", "DISEASE/TRAIT", "P-VALUE",
                       "PVALUE_MLOG"]

    def __init__(self, request_file):
        self.file = request_file
        self.original_name = request_file.name
        self.upload_name = f"{datetime.now().strftime('%Y_%m_%d_%X')}_{request_file.name}"

    def upload_file_locally(self):
        with open(f"SNP_App/uploads/{self.upload_name}", 'wb+') as destination:
            for chunk in self.file.chunks():
                destination.write(chunk)

    def has_all_fields(self):
        with open(f'SNP_App/uploads/{self.upload_name}', 'r') as read_obj:
            csv_dict_reader = DictReader(read_obj, delimiter="\t")
            column_names = csv_dict_reader.fieldnames
            for field in self.REQUIRED_FIELDS:
                if field not in column_names:
                    return False
            return True

    def clean_entries(self):
        uploaded_dataframe = pd.read_csv(f'SNP_App/uploads/{self.upload_name}',
                                         delimiter="\t",
                                         dtype={'CHR_ID': str, 'CHR_POS': str,
                                                'P-VALUE': float, 'PVALUE_MLOG': float})
        uploaded_dataframe = uploaded_dataframe.dropna(subset=self.REQUIRED_FIELDS)
        uploaded_dataframe = uploaded_dataframe[uploaded_dataframe.CHR_POS.apply(lambda x: x.isnumeric())]
        uploaded_dataframe['CHR_POS'] = uploaded_dataframe['CHR_POS'].astype(int)
        uploaded_dataframe['PVALUE_MLOG'] = uploaded_dataframe['PVALUE_MLOG'].round(2)
        clean_file_name = "cleaned_"+self.upload_name
        uploaded_dataframe.to_csv(path_or_buf=f'SNP_App/uploads/{clean_file_name}', sep="\t", index=False)
        self.upload_name = clean_file_name

    def upload_content_to_database(self):
        with open(f'SNP_App/uploads/{self.upload_name}', 'r') as read_obj:
            csv_dict_reader = DictReader(read_obj, delimiter="\t")
            for row in csv_dict_reader:

                snp_query = SNP.objects.filter(Rsid=row['SNPS'], Chrom_pos=row['CHR_POS'])
                if not snp_query:
                    SNP(Chrom=row['CHR_ID'], Chrom_pos=row['CHR_POS'], Rsid=row['SNPS']).save()

                disease_trait_query = DiseaseTrait.objects.filter(Disease_name=row['DISEASE/TRAIT'])
                if not disease_trait_query:
                    DiseaseTrait(Disease_name=row['DISEASE/TRAIT']).save()

                reference_query = Reference.objects.filter(Pubmedid=row['PUBMEDID'])
                if not reference_query:
                    Reference(Pubmedid=row['PUBMEDID'], Journal=row['JOURNAL'], Title=row['STUDY'],
                              Date=row['DATE']).save()

                snp_id = SNP.objects.get(Chrom_pos=row['CHR_POS'], Rsid=row['SNPS'])
                disease_trait_id = DiseaseTrait.objects.get(Disease_name=row['DISEASE/TRAIT'])
                reference_id = Reference.objects.get(Pubmedid=row['PUBMEDID'])
                association_query = Association.objects.filter(SNP=snp_id.Rsid,
                                                               Disease_trait=disease_trait_id.Disease_name,
                                                               Reference=reference_id.Pubmedid)
                if not association_query:
                    Association(SNP=snp_id, Disease_trait=disease_trait_id, Reference=reference_id,
                                Pvalue=row['P-VALUE'], Neglog10pvalue=row['PVALUE_MLOG']).save()
