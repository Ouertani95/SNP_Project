from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadFileForm

from upload_data import upload_file_locally


def display_home(request):
    return render(request, 'home.html')


def search_snp(request):
    return render(request, 'snp.html')


def search_phenotype(request):
    return render(request, 'phenotype.html')


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            file_name = upload_file_locally(request.FILES['file'])
            return HttpResponseRedirect("/success/")
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def upload_success(request):
    return render(request, 'success.html', {'message': "file uploaded successfully"})