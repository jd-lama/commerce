from django.shortcuts import render

# Create your views here.
def yos(request):
    return render(request,"yo/yo.html")