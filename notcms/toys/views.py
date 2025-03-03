from django.shortcuts import render


def barbell_app(request):
    return render(request, "toys/barbell.html")
