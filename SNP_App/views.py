from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UploadFileForm
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
