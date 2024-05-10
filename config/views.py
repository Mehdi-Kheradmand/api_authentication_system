from django.shortcuts import render


def home(req):
    return render(req, template_name="index.html")
