from django.db import models


class Case(models.Model):
    case_number = models.IntegerField(primary_key=True)
    person_name = models.CharField(max_length=30)
    identity_document_number = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    onset_date = models.DateField()
    date_confirmed = models.DateField()

    def __str__(self):
        return f"{self.case_number} {self.person_name}"


class Event(models.Model):
    classification_choices = [
    ('Infected', 'Infected'),
    ('Infector', 'Infector'),
    ('Both', 'Both'),
    ]
    case_number_name = models.ForeignKey(Case, on_delete=models.CASCADE)
    venue_name = models.CharField(max_length = 100)
    venue_location = models.CharField(max_length = 100)
    address = models.CharField(max_length = 300, null=True, blank=True)
    x_coord = models.FloatField(null=True, blank=True)
    y_coord = models.FloatField(null=True, blank=True)
    date_of_event = models.DateField()
    description = models.CharField(max_length = 200)
    classification = models.CharField(max_length=10, choices = classification_choices, default='Infected')

    def __str__(self):
        return self.venue_name
