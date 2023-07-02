from django.shortcuts import render, HttpResponse


def index(request):
    """Index page of the shop"""
    return HttpResponse('<div style="text-align: center;"><h1>Welcome to trenydol</h1></div>')
    # return render(request, 'vitrin/index.html')


def find_product(request):
    """Find the product that user wants to buy"""
    return HttpResponse('<div style="text-align: center;"><h1>This will be served for finding the product...</h1></div>')
