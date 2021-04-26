from django.shortcuts import render
from django.http import HttpResponse
import requests
from .models import Event, Case
from .forms import EventForm


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
    #test id
    # id = 1234
    case = Case.objects.get(pk=id)

    #Retrieve all events with matching id
    event_location_only = Event.objects.filter(case_number_name = id).values('venue_location')

    #Connect to API and update x coord, y coord and address
    for i in event_location_only:
        venue_loc = i['venue_location']
        query = {
            "q": venue_loc
        }
        response = requests.get("https://geodata.gov.hk/gs/api/v1.0.0/locationSearch?q=", params=query).json()
        x_val = response[0]['x']
        y_val = response[0]['y']
        address_val = response[0]['addressEN']
        Event.objects.filter(venue_location = venue_loc).update(address=address_val)
        Event.objects.filter(venue_location = venue_loc).update(x_coord=x_val)
        Event.objects.filter(venue_location = venue_loc).update(y_coord=y_val)

    events =  Event.objects.filter(case_number_name = id)
    context = {
        'case': case,
        'events': events
    }
    return render (request, 'case_expand.html', context)


def event(request, id):
    return HttpResponse(f"Event {id}")
