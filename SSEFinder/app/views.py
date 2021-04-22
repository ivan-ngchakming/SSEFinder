from django.shortcuts import render
from django.http import HttpResponse
from .models import Case


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
    return HttpResponse(f"Case {id}")


def event(request, id):
    return HttpResponse(f"Event {id}")
