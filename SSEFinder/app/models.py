from django.db import models


class Case(models.Model):
    case_number = models.IntegerField(primary_key=True)
    person_name = models.CharField(max_length=30)
    identity_document_number = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    onset_date = models.DateField()
    date_confirmed = models.DateField()

    def __str__(self):
        return f"{self.person_name}"
