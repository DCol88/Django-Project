from django.shortcuts import render

# Create your views here.
def get_index(request):
    return render(request, 'index.html')

def get_about(request):
    return render(request, 'about.html')

def get_video(request):
    return render(request, 'videos.html')