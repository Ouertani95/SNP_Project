from django.contrib import admin
from .models import SNP, Association, DiseaseTrait, Reference


@admin.register(SNP)
class SNPAdmin(admin.ModelAdmin):
    list_display = ('Rsid', 'Chrom', 'Chrom_pos')


@admin.register(DiseaseTrait)
class DiseaseTraitAdmin(admin.ModelAdmin):
    list_display = ('Disease_name',)


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('Pubmedid', 'Journal', 'Title', 'Date')


@admin.register(Association)
class AssociationAdmin(admin.ModelAdmin):
    list_display = ('SNP', 'Disease_trait', 'Reference', 'Pvalue', 'Neglog10pvalue')
