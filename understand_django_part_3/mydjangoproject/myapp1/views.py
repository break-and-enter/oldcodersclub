from django.shortcuts import render
from myapp1.models import Worker


def index_page(request):

    all_workers = Worker.objects.all()

    return render(request, 'index.html', {'data': all_workers})






def about_page(request):
    return render(request, 'about.html')


