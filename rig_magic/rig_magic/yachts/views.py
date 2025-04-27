from django.shortcuts import render

# Create your views here.

def dashboard(request):
    """
    Render the dashboard page.
    """
    context = {}
    return render(request, 'yachts/dashboard.html', context)