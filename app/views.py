from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta
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

        response_data['venue_name'] = venue_name
        response_data['venue_location'] = venue_location
        response_data['address'] = address
        response_data['x_coord'] = x_coord
        response_data['y_coord'] = y_coord
        response_data['date_of_event'] = date_of_event
        response_data['description'] = description

        try:
            event = Event.objects.get(venue_location=venue_location)
        except ObjectDoesNotExist:
            Event.objects.create(
                venue_name=venue_name,
                venue_location=venue_location,
                address=address,
                x_coord=x_coord,
                y_coord=y_coord,
                date_of_event=date_of_event,
                description=description,
            )
            event = Event.objects.get(venue_location=venue_location)

        case = Case.objects.get(case_number=case_number)

        print(f"onset date: {case.onset_date}")
        print(f"infected_status: ({case.onset_date - timedelta(days=14)} <= {event.date_of_event})")
        infected_status = case.onset_date - timedelta(days=14) <= event.date_of_event
        print(f"infector_status: ({case.onset_date - timedelta(days=3)} <= {event.date_of_event})")
        infector_status = case.onset_date - timedelta(days=3) <= event.date_of_event

        classification = Classification.objects.create(
            case=case,
            event=event,
            infected=infected_status,
            infector=infector_status,
        )
        classification.save()

        return JsonResponse(response_data)

    else:
        return render(request, 'showrecordform.html', {'events': events})


@login_required
def index(request):
    cases = Case.objects.all()

    context = {
        'cases': cases,
    }

    return render(request, "index.html", context)


@login_required
def case_detail(request):
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


@login_required
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


@login_required
def addcase(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CaseModelForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            print('123')
            # redirect to a new URL:

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CaseModelForm()
        case_number = request.GET.get('case_id', None)
        print('form ok')

    return render(request, 'addcase.html', {'form': form, 'case_no': case_number})


@login_required
def success(request):
    print('in success function')
    response_data = {}

    if request.method == 'POST':
        # CHANGED
        case_number = request.POST['case_number']
        personname = request.POST['person_name']
        idno = request.POST['identity_document_number']
        dob = request.POST['date_of_birth']
        onset = request.POST['onset_date']
        confirmdate = request.POST['date_confirmed']

        response_data['case_number'] = case_number
        response_data['person_name'] = personname
        response_data['identity_document_number'] = idno
        response_data['date_of_birth'] = dob
        response_data['onset_date'] = onset
        response_data['date_confirmed'] = confirmdate

        Case.objects.create(
            case_number=case_number,
            person_name=personname,
            identity_document_number=idno,
            date_of_birth=dob,
            onset_date=onset,
            date_confirmed=confirmdate
        )
        return JsonResponse(response_data)

    return render(request, 'index.html', {})


@login_required
def events(request):
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        if start_date == "" or end_date == "":
            events = Event.objects.filter(sse=True)
        else:
            events = Event.objects.filter(date_of_event__range=[start_date, end_date])

    else:
        events = Event.objects.filter(sse=True)

    # Update SSE status for every events to be displayed
    for event in events:
        event.identify_sse()

    context = {
        "events": events,
    }

    return render(request, "events.html", context)
