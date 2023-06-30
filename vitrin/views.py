from django.shortcuts import render, HttpResponse


def index(request):
    """Index page of the shop"""
    return HttpResponse('<div style="text-align: center;"><h1>Welcome to trenydol</h1></div>')
    # return render(request, 'vitrin/index.html')
