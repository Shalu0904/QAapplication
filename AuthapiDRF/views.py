from django.http import HttpResponse

def home_page(request):
    return HttpResponse("Welcome to the Home Page")
