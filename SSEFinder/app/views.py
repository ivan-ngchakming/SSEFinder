from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "index.html", {})


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
