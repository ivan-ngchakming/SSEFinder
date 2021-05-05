import requests
from django.db import models


class Case(models.Model):
    case_number = models.IntegerField(primary_key=True)
    person_name = models.CharField(max_length=30)
    identity_document_number = models.CharField(max_length=30, unique=True)
    date_of_birth = models.DateField()
    onset_date = models.DateField()
    date_confirmed = models.DateField()

    def __str__(self):
        return f"{self.case_number} {self.person_name}"


class Event(models.Model):
    venue_name = models.CharField(max_length=100)
    venue_location = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=300, null=True, blank=True)  # Auto updated via api
    x_coord = models.FloatField(null=True, blank=True)  # Auto updated via api
    y_coord = models.FloatField(null=True, blank=True)  # Auto updated via api
    date_of_event = models.DateField()
    description = models.CharField(max_length=200)
    sse = models.BooleanField(default=False)

    def identify_sse(self):
        """Update sse status of event"""
        SSE_THRESHOLD = 6
        classifications = self.classification_set.all()
        if len(classifications) > SSE_THRESHOLD and not self.sse:
            self.sse = True
            self.save()
        elif len(classifications) <= SSE_THRESHOLD and self.sse:
            self.sse = False
            self.save()

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
        classification = self.classification_set.get(case_id=case_number)

        result = []
        if classification.infector:
            result.append("Infector")
        if classification.infected:
            result.append("Infected")

        return result

    def get_classification_str(self, case_number):
        return ", ".join(self.get_classification(case_number))

    def __str__(self):
        return f"{self.venue_name}, {self.venue_location}"


class Classification(models.Model):
    infected = models.BooleanField()
    infector = models.BooleanField()
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.case} - {self.event}"
