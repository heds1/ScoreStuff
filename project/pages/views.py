from django.shortcuts import render

def home(request):
    return render(request, template_name='pages/home.html')


def privacy(request):
    return render(request, template_name='pages/privacy.html')