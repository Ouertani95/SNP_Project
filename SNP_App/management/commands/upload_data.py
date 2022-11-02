from django.core.management.base import BaseCommand

from SNP_App.scripts.upload_data import FileUploader


class Command(BaseCommand):
    help = 'Uploads data from file to database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs=1, type=str)

    def handle(self, *args, **options):
        file_path = options['file_path'][0]
        self.stdout.write(file_path)
        file_uploader = FileUploader(file_path, cli_input=True)
        if file_uploader.file_is_tsv():
            self.stdout.write("Uploading file ...")
            file_uploader.upload_file_locally()
            self.stdout.write("File uploaded successfully !")
            if file_uploader.has_all_fields():
                self.stdout.write("Cleaning data ...")
                file_uploader.clean_entries()
                self.stdout.write("Data successfully cleaned !")
                self.stdout.write("Uploading to database ...")
                file_uploader.upload_content_to_database()
                self.stdout.write("Data successfully uploaded to database !")
                self.stdout.write("Removing uploaded files ...")
                file_uploader.remove_files()
                self.stdout.write("Files removed successfully !")
            else:
                self.stdout.write("Wrong file format !\n"
                                  "Please verify that your file contains at least the following fields:\n"
                                  "PUBMEDID, JOURNAL, STUDY, DATE, CHR_ID, CHR_POS, SNPS, "
                                  "DISEASE/TRAIT, P-VALUE, PVALUE_MLOG")
                self.stdout.write("Removing uploaded files ...")
                file_uploader.remove_files()
                self.stdout.write("Files removed successfully !")
        else:
            self.stdout.write("Wrong file format ! Please use a tsv file.")
