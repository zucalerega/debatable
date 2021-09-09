from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Resource
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
#from bs4 import BeautifulSoup
#import requests

class ResourceListView(ListView):
    model=Resource
    template_name='resources/resources.html'
    context_object_name='resources'
    ordering=['-type']
    #posts per page
class ResourceDetailView(LoginRequiredMixin, DetailView):
    template_name='resources/resources.html'
    model=Resource

def get_resources(topic):
    resource_list = {}
    topic=topic.replace(' ', '+')
    page = requests.get('https://scholar.google.com/scholar?hl=en&as_sdt=0%2C14&as_ylo=2017&q='+topic+'&btnG=')
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all("div", class_='gs_ri')
    for i in results:
        if len(Resource.objects.filter(link=i.find("a")['href'])) == 0:
            Resource.objects.create(
            title=i.find('h3', 'gs_rt').find("a").text.strip(),
            link=i.find('h3', 'gs_rt').find("a")['href'],
            author=i.find('div', class_='gs_a').text.strip(),
            style='Scholarly',
            content=i.find('div', class_='gs_rs').text.strip(),
            type=topic
            )
    return None
    # Print out most recent articles

    return None
def resource_list_view(request):
    r_list = []
    for i in ['Healthcare', 'Gun Rights', 'Voting Rights', 'Economic Systems', 'Abortion', "Foreign Policy"]:
        get_resources(i)

        r_list.append(Resource.objects.filter(type=i))
    context = {'resources': r_list}
    return render(request, 'resources/resources.html', context)
