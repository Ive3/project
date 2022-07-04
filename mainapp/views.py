from django.shortcuts import render
# Create your views here.


def index(request):
    return render(request, 'mainapp/index.html')

def check():
    pass


def my_error404(request, exception):
    return render(request, 'mainapp/404.html')
    

def my_error403(request, exception):
    return render(request, 'mainapp/403.html')

def my_error500(request):
    return render(request, 'mainapp/500.html')