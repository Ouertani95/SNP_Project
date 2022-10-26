from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django_serverside_datatable.views import ServerSideDatatableView

from .forms import UploadFileForm
from .models import SNP, DiseaseTrait, Association
from .scripts.upload_data import FileUploader


def display_home(request):
    return render(request, 'home.html')


def search_snp(request):
    return render(request, 'snp.html')


def search_phenotype(request):
    return render(request, 'phenotype.html')


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
                return redirect("/success/")
            else:
                return redirect("/error/")
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def upload_success(request):
    return render(request, 'success.html')


def upload_error(request):
    return render(request, 'error.html')


class SNPListView(ServerSideDatatableView):
    queryset = SNP.objects.all()
    columns = ['Chrom', 'Chrom_pos', 'Rsid']


class DiseaseTraitListView(ServerSideDatatableView):
    queryset = DiseaseTrait.objects.all()
    columns = ['Disease_name']


def phenotype_details(request, name):
    phenotype_query = Association.objects.filter(Disease_trait_id=name)
    return render(request, 'phenotype_details.html', {'details': phenotype_query, 'name': name})


def snp_details(request, rsid):
    snp_query = Association.objects.filter(SNP_id=rsid)
    return render(request, 'snp_details.html', {'details': snp_query, 'rsid': rsid})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def services(request):
    return render(request, 'services.html')

