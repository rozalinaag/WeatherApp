from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm


def index(request):
    appid = 'a95f569d3ab8b0215b97f723a678920e'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    if (request.method == 'POST'):
        if request.POST.get("send") == 'search':
            if not City.objects.filter(name=request.POST.get("name")).exists():
                form = CityForm(request.POST)
                form.save()
        else:
            # method for delete
            City.objects.filter(name=request.POST.get("delete")).delete()

    form = CityForm()  # for clean form "enter city"

    cities = City.objects.all()

    all_cities = []
    for city in cities:
        res = requests.get(url.format(city.name)).json()  # преобразовываем джейсон формат в привычный словарь
        city_info = {
            'city': city.name,
            'temp': res['main']["temp"],
            'icon': res["weather"][0]["icon"],
        }
        all_cities.append(city_info)

    context = {
        'all_info': all_cities,
        'form': form
    }

    return render(request, 'weather/index.html', context)



def information(request):
    return render(request, 'weather/information.html')
