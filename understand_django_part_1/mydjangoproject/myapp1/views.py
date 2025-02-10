from django.shortcuts import render


def index_page(request):
    return render(request, 'index.html')


def about_page(request):






    return render(request, 'about.html')