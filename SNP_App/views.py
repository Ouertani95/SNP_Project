from django.shortcuts import render


def display_base(request):
    return render(request, 'home.html')


def search_snp(request):
    return render(request, 'snp.html')


def search_phenotype(request):
    return render(request, 'phenotype.html')
