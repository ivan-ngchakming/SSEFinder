from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Event, Case
from .forms import CaseModelForm


@login_required
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


@login_required
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
        caseno = request.POST['caseno']
        personname = request.POST['person_name']
        idno = request.POST['identity_document_number']
        dob = request.POST['date_of_birth']
        onset = request.POST['onset_date']
        confirmdate = request.POST['date_confirmed']

        response_data['case_number'] = caseno
        response_data['person_name'] = personname
        response_data['identity_document_number'] = idno
        response_data['date_of_birth'] = dob
        response_data['onset_date'] = onset
        response_data['date_confirmed'] = confirmdate

        Case.objects.create(case_number=caseno,person_name=personname,identity_document_number=idno,date_of_birth=dob,onset_date=onset,date_confirmed=confirmdate)
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
