from django.views.generic import TemplateView
from django.shortcuts import render


class HomePageView(TemplateView):
    template_name = 'index.html'

def custom_404(request, exception):
    return render(request, "404.html", status=404)