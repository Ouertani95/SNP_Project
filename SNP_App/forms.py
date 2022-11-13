from django import forms
from django.core.validators import RegexValidator
from SNP_App.models import SNP


class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={"class": "form-control mt-4"}),
                           label="SNP/Phenotype associations file")


def get_choices():
    chroms_query = SNP.objects.all().values('Chrom').distinct()
    choices = []
    if chroms_query:
        chroms = [chrom["Chrom"] for chrom in chroms_query]
        alpha_list = []
        for chrom in chroms:
            if chrom.isalpha():
                alpha_list.append(chrom)
                chroms.remove(chrom)
        chroms.sort(key=int)
        alpha_list.sort()
        chroms = chroms + alpha_list
        choices = [(chrom, chrom) for chrom in chroms]
    return choices


class SnpSearchChromForm(forms.Form):
    choices = get_choices()
    chromosome = forms.ChoiceField(label="Select chromosome", choices=choices,
                                   widget=forms.Select(attrs={"class": "form-select"}))
    region = forms.CharField(widget=forms.Textarea(attrs={"rows": 2, "cols": 20, "class": "form-control"}),
                             help_text="Example : 4448:11264851", required=False,
                             validators=[RegexValidator(regex='^[0-9]+:[0-9]+$',
                                                        message="Only the following format is allowed :"
                                                                "\n xxxxxx:yyyyyy ")])


class SnpSearchRsidForm(forms.Form):
    rsid = forms.CharField(widget=forms.Textarea(attrs={"rows": 2, "cols": 20, "class": "form-control"}),
                           help_text="Example : rs1002655 rs100537")
