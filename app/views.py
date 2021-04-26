import requests
from django.http import HttpResponse
from django.shortcuts import render

from .models import Event, Case, Classification


def index(request):
    # Create dummy data
    # from faker import Faker
    # fake = Faker()
    # for i in range(10):
    #     new_case = Case()
    #     new_case.case_number = i
    #     new_case.person_name = fake.name()
    #     new_case.identity_document_number = fake.isbn10()
    #     new_case.date_of_birth = fake.date_object()
    #     new_case.onset_date = fake.date_object()
    #     new_case.date_confirmed = fake.date_object()
    #     new_case.save()

    cases = Case.objects.all()

    context = {
        'cases': cases,
    }

    return render(request, "index.html", context)


def login(request):
    return HttpResponse("Login")


def cases(request):
    return HttpResponse("Cases")


def events(request):
    return HttpResponse("Superspreading Events")


def case(request, id):
    # Create Dummy Event data
    # locations = [
    #     ("Kam Lok Hin Chicken and Fish Pot", "Conwell Mansion"),
    #     ("Dynasty II", "The Dynasty Club"),
    #     ("Hong Kong Cultural Centre Administration Building", "Hong Kong Cultural Centre Administration Building"),
    #     ("The Flying Frenchman", "The Flying Frenchman"),
    # ]
    # from faker import Faker
    # fake = Faker()
    # for location in locations:
    #     new_event = Event()
    #     new_event.venue_name = location[0]
    #     new_event.venue_location = location[1]
    #     new_event.date_of_event = fake.date_object()
    #     new_event.description = fake.text(200)
    #     new_event.save()
    #
    # cases = Case.objects.all()
    # events = Event.objects.all()
    # for i, case in enumerate(cases):
    #     for j, event in enumerate(events):
    #         if i == j:
    #             new_class = Classification(
    #                 infected=True,
    #                 infector=True,
    #                 case=case,
    #                 event=event
    #             )
    #             new_class.save()
    #         if i > j:
    #             new_class = Classification(
    #                 infected=True,
    #                 infector=False,
    #                 case=case,
    #                 event=event
    #             )
    #             new_class.save()
    # Dummy data entry end

    case = Case.objects.get(pk=id)
    all_classifications = case.classification_set.all()
    events = [classification.event for classification in all_classifications]
    classifications = [event.get_classification_str(case.case_number) for event in events]
    events = list(zip(events, classifications))

    context = {
        'case': case,
        'events': events,
    }

    return render(request, 'case_expand.html', context)


def event(request, id):
    return HttpResponse(f"Event {id}")