from django.db import models


class SNP(models.Model):
    Chrom = models.CharField(max_length=100)
    Chrom_pos = models.PositiveIntegerField(unique=True)
    Rsid = models.CharField(max_length=100, unique=True)


class Reference(models.Model):
    Pubmedid = models.PositiveIntegerField(unique=True)
    Journal = models.CharField(max_length=100)
    Title = models.CharField(max_length=1000, unique=True)
    Date = models.DateField()


class DiseaseTrait(models.Model):
    Disease_name = models.CharField(max_length=100, unique=True)


class Association(models.Model):
    SNP = models.ForeignKey(SNP, on_delete=models.CASCADE)
    Disease_trait = models.ForeignKey(DiseaseTrait, on_delete=models.CASCADE)
    Reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    Pvalue = models.FloatField()
    Neglog10pvalue = models.FloatField()
