from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField(label="SNP/Phenotype associations file")
