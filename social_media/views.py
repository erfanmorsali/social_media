from django.shortcuts import render, HttpResponse


def home_page(request):
    return render(request,"home_page.html")
