from datetime import datetime
from csv import DictReader
from SNP_App.models import SNP, Reference, DiseaseTrait, Association


class FileUploader:
    REQUIRED_FIELDS = ["DISEASE/TRAIT", "PUBMEDID", "JOURNAL", "STUDY", "DATE", "CHR_ID", "CHR_POS", "SNPS", "P-VALUE",
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
        # open file in read mode
        with open(f'SNP_App/uploads/{self.upload_name}', 'r') as read_obj:
            # pass the file object to DictReader() to get the DictReader object
            csv_dict_reader = DictReader(read_obj, delimiter="\t")
            # get column names from a csv file
            column_names = csv_dict_reader.fieldnames
            print(column_names)
            for field in self.REQUIRED_FIELDS:
                if field not in column_names:
                    print(field)
                    return False
            return True

    def upload_content_to_database(self):

        # open file in read mode
        with open(f'SNP_App/uploads/{self.upload_name}', 'r') as read_obj:
            # pass the file object to DictReader() to get the DictReader object
            csv_dict_reader = DictReader(read_obj, delimiter="\t")
            # iterate over each line as an ordered dictionary
            for row in csv_dict_reader:
                # check if snp does not exist in database
                snp_query = SNP.objects.filter(Rsid=row['SNPS'], Chrom_pos=row['CHR_POS'])
                if not snp_query:
                    SNP(Chrom=row['CHR_ID'], Chrom_pos=row['CHR_POS'], Rsid=row['SNPS']).save()
                # check if disease/trait does not exist in database
                disease_trait_query = DiseaseTrait.objects.filter(Disease_name=row['DISEASE/TRAIT'])
                if not disease_trait_query:
                    DiseaseTrait(Disease_name=row['DISEASE/TRAIT']).save()
                # check if reference does not exist in database
                reference_query = Reference.objects.filter(Pubmedid=row['PUBMEDID'])
                if not reference_query:
                    Reference(Pubmedid=row['PUBMEDID'], Journal=row['JOURNAL'], Title=row['STUDY'],
                              Date=row['DATE']).save()
                snp_id = SNP.objects.get(Chrom_pos=row['CHR_POS'], Rsid=row['SNPS'])
                disease_trait_id = DiseaseTrait.objects.get(Disease_name=row['DISEASE/TRAIT'])
                reference_id = Reference.objects.get(Pubmedid=row['PUBMEDID'])
                association_query = Association.objects.filter(SNP=snp_id.id, Disease_trait=disease_trait_id.id,
                                                               Reference=reference_id.id)
                if not association_query:
                    Association(SNP=snp_id, Disease_trait=disease_trait_id, Reference=reference_id,
                                Pvalue=row['P-VALUE'], Neglog10pvalue=row['PVALUE_MLOG']).save()
