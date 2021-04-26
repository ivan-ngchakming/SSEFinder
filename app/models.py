import requests
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
    venue_name = models.CharField(max_length=100)
    venue_location = models.CharField(max_length=100)
    address = models.CharField(max_length=300, null=True, blank=True)  # Auto updated via api
    x_coord = models.FloatField(null=True, blank=True)  # Auto updated via api
    y_coord = models.FloatField(null=True, blank=True)  # Auto updated via api
    date_of_event = models.DateField()
    description = models.CharField(max_length=200)

    def update_geodata(self):
        """Connect to API and update x coord, y coord and address"""
        query = {
            "q": self.venue_location
        }

        response = requests.get(
            "https://geodata.gov.hk/gs/api/v1.0.0/locationSearch?q=",
            params=query,
        ).json()

        self.x_coord = response[0]['x']
        self.y_coord = response[0]['y']
        self.address = response[0]['addressEN']

    def get_classification(self, case_number):
        classifications = self.classification_set.all()
        classification = [c for c in classifications if c.case.case_number == case_number]

        if len(classification) > 1:
            raise IndexError("Something has gone wrong")
        else:
            classification = classification[0]

        result = []
        if classification.infector:
            result.append("Infector")
        if classification.infected:
            result.append("Infected")

        return result

    def get_classification_str(self, case_number):
        return ", ".join(self.get_classification(case_number))

    def __str__(self):
        return self.venue_name


class Classification(models.Model):
    infected = models.BooleanField()
    infector = models.BooleanField()
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.case
