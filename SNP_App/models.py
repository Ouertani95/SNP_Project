from django.db import models


class SNP(models.Model):
    Chrom = models.CharField(max_length=100)
    Chrom_pos = models.PositiveIntegerField()
    Rsid = models.CharField(max_length=100)


class Reference(models.Model):
    Pubmedid = models.PositiveIntegerField()
    Journal = models.CharField(max_length=100)
    Title = models.CharField(max_length=1000)
    Date = models.DateField()


class DiseaseTrait(models.Model):
    Disease_name = models.CharField(max_length=100)


class SNP2Phenotype2Ref(models.Model):
    SNP_id = models.ForeignKey(SNP, on_delete=models.CASCADE)
    Disease_trait_id = models.ForeignKey(DiseaseTrait, on_delete=models.CASCADE)
    Reference_id = models.ForeignKey(Reference, on_delete=models.CASCADE)
    Pvalue = models.FloatField()
    Neglog10pvalue = models.FloatField()
