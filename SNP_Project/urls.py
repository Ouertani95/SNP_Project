"""SNP_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from SNP_App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.display_home, name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('upload/', views.upload_file, name='upload'),
    path('snp_search/', views.search_snp, name='snp_search'),
    path('snp_json/', views.SNPListView.as_view(), name='snp_json'),
    path('snp/details/<str:rsid>/', views.snp_details, name='snp_details'),
    path('phenotype_search/', views.pheno_auto_search, name='pheno_auto_search'),
    path('pheno_autocomplete/', views.pheno_autocomplete, name='pheno_autocomplete'),
    path('phenotype_list/', views.search_phenotype, name='phenotype_list'),
    path('pheno_json/', views.DiseaseTraitListView.as_view(), name='pheno_json'),
    path('phenotype/details/<str:name>/', views.phenotype_details, name='pheno_details'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
