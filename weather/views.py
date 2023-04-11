from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
# Create your views here.
def index(request): 
    url  = "https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=PLACE_YOUR_KEY"
    #handles input from the user
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
    form = CityForm()

    weather_data = []
    cities = City.objects.all()
    
    for city in cities:  
        city_weather = requests.get(url.format(city)).json()
        # print(city_weather)
        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon'],
          }
        weather_data.append(weather) #adds current data to the list
    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/index.html', context)

