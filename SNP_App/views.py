from django.contrib.auth.decorators import login_required
from django.db.models import Min
from django.shortcuts import render, redirect
from django_serverside_datatable.views import ServerSideDatatableView

from .forms import UploadFileForm
from .models import SNP, DiseaseTrait, Association
from .scripts.upload_data import FileUploader


def display_home(request):
    return render(request, 'home.html', {'title': "Home"})


def search_snp(request):
    return render(request, 'snp.html', {'title': "SNP search"})


def search_phenotype(request):
    return render(request, 'phenotype.html', {'title': "Phenotype Search"})


@login_required(login_url='/login/')
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            file_uploader = FileUploader(request.FILES['file'])
            file_uploader.upload_file_locally()
            if file_uploader.has_all_fields():
                file_uploader.clean_entries()
                file_uploader.upload_content_to_database()
                file_uploader.remove_files()
                return redirect("/success/")
            else:
                file_uploader.remove_files()
                return redirect("/error/")
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form, 'title': "upload"})


def upload_success(request):
    return render(request, 'success.html', {'title': "success"})


def upload_error(request):
    return render(request, 'error.html', {'title': "error"})


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
