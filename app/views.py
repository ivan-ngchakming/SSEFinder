import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Event, Case, Classification
from django.core.exceptions import ObjectDoesNotExist


# TRIAL FORM SUBMISSION
def create_post(request):
    response_data = {}
    if request.method == 'POST':
        print("Processing post request")
        venue_name = request.POST.get('venue_name', None)  # getting data from venue_name input
        venue_location = request.POST.get('venue_location', None)  # getting data from venue_location input
        address = request.POST.get('address', None)  # getting data from address input
        x_coord = request.POST.get('x_coord', None)  # getting data from x_coord input
        y_coord = request.POST.get('y_coord', None)  # getting data from y_coord input
        date_of_event = request.POST.get('date_of_event', None)  # getting data from date_of_event input
        description = request.POST.get('description', None)  # getting data from description input
        case_number = request.POST.get('case_number', None)

        response_data['venue_name'] = venue_name
        response_data['venue_location'] = venue_location
        response_data['address'] = address
        response_data['x_coord'] = x_coord
        response_data['y_coord'] = y_coord
        response_data['date_of_event'] = date_of_event
        response_data['description'] = description

        # response data for Classification
        # case = request.POST.get('case', None)
        # response_data['case'] = case
        # end of response data for Classification

        try:
            event = Event.objects.get(venue_location=venue_location)
        except ObjectDoesNotExist:
            event = Event.objects.create(
                venue_name=venue_name,
                venue_location=venue_location,
                address=address,
                x_coord=x_coord,
                y_coord=y_coord,
                date_of_event=date_of_event,
                description=description,
            )
            event.save()
        classification = Classification.objects.create(
            case=Case.objects.get(case_number=case_number),
            event=event,
            infected=True,
            infector=False,
        )
        classification.save()

        return JsonResponse(response_data)

    else:
        return render(request, 'showrecordform.html', {'events': events})


# END OF TRIAL FORM SUBMISSION

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


def case_detail(request):
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
    # for event in events:
    #     event.update_geodata()
    #     event.save()
    # Dummy data entry end

    case_number = request.GET.get('case_number', None)

    case = Case.objects.get(pk=case_number)
    all_classifications = case.classification_set.all()
    events = [classification.event for classification in all_classifications]
    classifications = [event.get_classification_str(case.case_number) for event in events]
    events = list(zip(events, classifications))

    context = {
        'case': case,
        'events': events,

    }

    return render(request, "case_detail.html", context)


def login(request):
    return HttpResponse("Login")


def events(request):
    events = Event.objects.all()

    # Update SSE status for all events
    for event in events:
        event.identify_sse()

    context = {
        'events': [e for e in events if e.sse],
    }
    return render(request, "events.html", context)


def event_detail(request):
    event_name = request.GET.get('event_name', None)

    event = Event.objects.get(venue_name=event_name)
    all_classifications = event.classification_set.all()
    cases = [classification.case for classification in all_classifications]
    classifications = [event.get_classification_str(case.case_number) for case in cases]
    cases = list(zip(cases, classifications))

    context = {
        'cases': cases,
    }

    return render(request, "event_detail.html", context)
