from django.contrib.auth.decorators import login_required
from django.db.models import Min
from django.http import JsonResponse
from django.shortcuts import render
from django_serverside_datatable.views import ServerSideDatatableView

from .forms import UploadFileForm, SnpSearchChromForm, SnpSearchRsidForm
from .models import SNP, DiseaseTrait, Association
from .scripts.upload_data import FileUploader


def display_home(request):
    return render(request, 'home.html', {'title': "Home"})


def search_snp(request):
    chrom_search_form = SnpSearchChromForm()
    rsid_search_form = SnpSearchRsidForm()
    if request.method == "POST":
        form_id = request.POST.get("formId")
        if form_id == "snp_chrom_search":
            form = SnpSearchChromForm(request.POST)
            if form.is_valid():
                chrom = request.POST.get("chromosome")
                region = request.POST.get("region")
                if region:
                    region = region.strip()
                    region = region.split(":")
                    if int(region[0]) > int(region[1]):
                        error = "Region : Start position can't be bigger than end position."
                        return render(request, 'snp_search_forms.html', {'title': "SNP search",
                                                                         'chrom_form': chrom_search_form,
                                                                         'rsid_form': rsid_search_form,
                                                                         'errors': error})
                    query = SNP.objects.filter(Chrom=chrom, Chrom_pos__range=(region[0], region[1]))
                else:
                    query = SNP.objects.filter(Chrom=chrom)
                return render(request, 'snp.html', {"results": query})

            else:
                return render(request, 'snp_search_forms.html', {'title': "SNP search",
                                                                 'chrom_form': chrom_search_form,
                                                                 'rsid_form': rsid_search_form,
                                                                 'errors': form.errors})
        else:
            form = SnpSearchRsidForm(request.POST)
            rsid_string = request.POST.get("rsid")
            rsid_string = rsid_string.strip()
            rsid_list = rsid_string.split(" ")
            query = SNP.objects.filter(Rsid__in=rsid_list)
            if form.is_valid():
                return render(request, 'snp.html', {"results": query})

    else:
        return render(request, 'snp_search_forms.html', {'title': "SNP search",
                                                         'chrom_form': chrom_search_form,
                                                         'rsid_form': rsid_search_form})


def search_phenotype(request):
    return render(request, 'phenotype_list.html', {'title': "Phenotype explore"})


@login_required(login_url='/login/')
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_uploader = FileUploader(request.FILES['file'], cli_input=False)
            if file_uploader.file_is_tsv():
                file_uploader.upload_file_locally()
                if file_uploader.has_all_fields():
                    file_uploader.clean_entries()
                    file_uploader.upload_content_to_database()
                    file_uploader.remove_files()
                    return JsonResponse({"error": "", "success": "Data successfully added to database"})
                else:
                    file_uploader.remove_files()
                    return JsonResponse({"error": "Wrong file format !<br>"
                                                  "Please verify that your file contains at least the following fields:"
                                                  "<br> "
                                                  "PUBMEDID, JOURNAL, STUDY, DATE, CHR_ID, CHR_POS, SNPS, "
                                                  "DISEASE/TRAIT, P-VALUE,PVALUE_MLOG",
                                         "success": ""})
            else:
                return JsonResponse({"error": "Wrong file format !<br>Please use a tsv file.", "success": ""})

    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form, 'title': "upload"})


class SNPListView(ServerSideDatatableView):
    queryset = SNP.objects.all()
    columns = ['Rsid', 'Chrom', 'Chrom_pos']


class DiseaseTraitListView(ServerSideDatatableView):
    queryset = DiseaseTrait.objects.all()
    columns = ['Disease_name']


def phenotype_details(request, name):
    phenotype_query = Association.objects.filter(Disease_trait_id=name)
    min_pvalue = phenotype_query.aggregate(Min('Pvalue'))
    snp_min_pvalue = phenotype_query.filter(Pvalue=min_pvalue['Pvalue__min'])
    number_studies = phenotype_query.values('Reference').distinct().count()
    return render(request, 'phenotype_details.html',
                  {'details': phenotype_query, 'detail_name': name, 'detail_type': 'Phenotype',
                   'title': name, 'studies': number_studies, 'min_pvalue': min_pvalue,
                   'snp_min_pvalue': snp_min_pvalue})


def snp_details(request, rsid):
    association_query = Association.objects.filter(SNP_id=rsid)
    snp_query = SNP.objects.get(Rsid=rsid)
    min_pvalue = association_query.aggregate(Min('Pvalue'))
    phenotype_min_pvalue = association_query.filter(Pvalue=min_pvalue['Pvalue__min'])
    number_studies = association_query.values('Reference').distinct().count()
    return render(request, 'snp_details.html',
                  {'details': association_query, 'detail_name': rsid, 'detail_type': 'SNP',
                   'title': rsid, 'studies': number_studies, 'snp': snp_query,
                   'min_pvalue': min_pvalue, 'phenotype_min_pvalue': phenotype_min_pvalue})


def about(request):
    return render(request, 'about.html', {'title': "About"})


def contact(request):
    return render(request, 'contact.html', {'title': "Contact"})


def services(request):
    return render(request, 'services.html', {'title': "Services"})


def pheno_autocomplete(request):
    search = request.GET.get('search')
    payload = []
    if search and len(search) >= 3:
        traits = DiseaseTrait.objects.filter(Disease_name__icontains=search)
        for trait in traits:
            payload.append({'trait': trait.Disease_name})
    return JsonResponse({
        'status': True,
        'payload': payload
    })


def pheno_auto_search(request):
    return render(request, 'phenotype_search.html', {'title': "Phenotype search"})
