from django.http import HttpResponse


def index(request):
    return HttpResponse("<h1> PUBLIC TENANT <h1/>")
