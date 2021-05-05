from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from datetime import timedelta, datetime
from .models import Event, Case, Classification
from .forms import CaseModelForm


@login_required
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

        case = Case.objects.get(case_number=case_number)
        response_data['date_start'] = case.onset_date - timedelta(days=14)
        response_data['date_end'] = case.date_confirmed

        identifier = f"{venue_name}, {venue_location}, {date_of_event}"
        event = [event for event in Event.objects.all() if event.identifier == identifier]

        if len(event) == 1:
            event = event[0]
            if case.onset_date - timedelta(days=14) > event.date_of_event or case.date_confirmed < event.date_of_event:
                response_data['date_valid'] = False
                response_data['event_exist'] = True
                response_data['venue_name'] = event.venue_name
                response_data['date_of_event'] = event.date_of_event
                response_data['description'] = event.description
            else:
                response_data['date_valid'] = True

        elif len(event) == 0:
            event_date_object = datetime.strptime(date_of_event, "%Y-%m-%d").date()
            if case.onset_date - timedelta(days=14) > event_date_object or case.date_confirmed < event_date_object:
                response_data['date_valid'] = False
                response_data['event_exist'] = False
            else:
                response_data['date_valid'] = True
                Event.objects.create(
                    venue_name=venue_name,
                    venue_location=venue_location,
                    address=address,
                    x_coord=x_coord,
                    y_coord=y_coord,
                    date_of_event=date_of_event,
                )
                event = [event for event in Event.objects.all() if event.identifier == identifier]
        else:
            raise Exception("Something went wrong")

        if response_data['date_valid']:
            infected_status = case.onset_date - timedelta(days=14) <= event.date_of_event
            infector_status = case.onset_date - timedelta(days=3) <= event.date_of_event

            classification = Classification.objects.create(
                case=case,
                event=event,
                infected=infected_status,
                infector=infector_status,
                description=description,
            )
            classification.save()

        return JsonResponse(response_data)

    else:
        return render(request, 'showrecordform.html', {'events': events})


@login_required
def index(request):
    cases = sorted(Case.objects.all(), key=lambda x: x.onset_date)

    context = {
        'cases': cases,
    }

    return render(request, "index.html", context)


@login_required
def case_detail(request):
    case_number = request.GET.get('case_number', None)

    case = Case.objects.get(pk=case_number)
    all_classifications = sorted(case.classification_set.all(), key=lambda x: x.event.date_of_event)
    events = [classification.event for classification in all_classifications]
    classifications = [event.get_classification_str(case.case_number) for event in events]
    descriptions = [classification.description for classification in all_classifications]
    events = list(zip(events, classifications, descriptions))

    context = {
        'case': case,
        'events': events,
    }

    return render(request, "case_detail.html", context)


@login_required
def event_detail(request):
    event_name = request.GET.get('event_name', None)
    event_location = request.GET.get('event_location', None)
    date_of_event = request.GET.get('date_of_event', None)

    identifier = f"{event_name}, {event_location}, {date_of_event}"
    event = [event for event in Event.objects.all() if event.identifier == identifier][0]

    all_classifications = event.classification_set.all()
    cases = [classification.case for classification in all_classifications]
    classifications = [event.get_classification_str(case.case_number) for case in cases]
    descriptions = [classification.description for classification in all_classifications]
    cases = list(zip(cases, classifications, descriptions))

    context = {
        'cases': cases,
    }

    return render(request, "event_detail.html", context)


@login_required
def addcase(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        case_number = request.POST.get('case_number', None)
        personname = request.POST.get('person_name', None)
        idno = request.POST.get('identity_document_number', None)
        dob = request.POST.get('date_of_birth', None)
        onset = request.POST.get('onset_date', None)
        confirmdate = request.POST.get('date_confirmed', None)

        response_data = {}
        if case_number == "" or personname == "" or idno == "" or  dob == "" or  onset == "" or  confirmdate == "":
            response_data['success'] = False
            response_data['error_msg'] = "Please fill in all fields."
            return JsonResponse(response_data)
        else:
            try:
                Case.objects.create(
                    case_number=case_number,
                    person_name=personname,
                    identity_document_number=idno,
                    date_of_birth=dob,
                    onset_date=onset,
                    date_confirmed=confirmdate
                )
                response_data['success'] = True
            except IntegrityError as e:
                response_data['success'] = False
                response_data['error_msg'] = "Error: " + str(e.__cause__)

            return JsonResponse(response_data)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CaseModelForm()
        case_number = request.GET.get('case_id', None)

    return render(request, 'addcase.html', {'form': form, 'case_no': case_number})


@login_required
def events(request):
    # Update SSE status for every events to be displayed
    events = Event.objects.all()
    for event in events:
        event.identify_sse()

    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        if start_date == "" or end_date == "":
            events = Event.objects.filter(sse=True)
        else:
            events = Event.objects.filter(date_of_event__range=[start_date, end_date])
            events = [event for event in events if event.sse]

    else:
        events = Event.objects.filter(sse=True)

    context = {
        "events": events,
    }

    return render(request, "events.html", context)
