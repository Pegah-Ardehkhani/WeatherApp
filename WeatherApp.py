from tkinter import *
import requests
import json
from datetime import datetime
from PIL import Image,ImageTk
 
# Initialize Window
 
root = Tk()
root.geometry('450x550') #size of the window by default
root.resizable(0,0) #to make the window size fixed
root.title('Weather Info') #title of our window
root.configure(bg='#adebeb')

# ----------------------Functions to fetch and display weather info
city_value = StringVar()
 
def time_format_for_location(utc_with_tz):
    local_time = datetime.utcfromtimestamp(utc_with_tz)
    return local_time.time()
 
city_value = StringVar()
 
def showWeather():
    # api key, copied from the OpenWeatherMap dashboard
    api_key = '3f93bb4793eca5b59822cd640573113c'
 
    # Get city name from user from the input field (later in the code)
    city_name = city_value.get()
 
    # API url
    weather_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city_name + '&appid=' + api_key
 
    # Get the response from fetched url
    response = requests.get(weather_url)
 
    # changing response from json to python readable 
    weather_info = response.json()
 
    tfield.delete('1.0', 'end')   # to clear the text field for every new output

# as per API documentation, if the cod is 200, it means that weather data was successfully fetched
  
    if weather_info['cod'] == 200:
        kelvin = 273 # value of kelvin

# -----------Storing the fetched values of weather of a city
 
        temp = int(weather_info['main']['temp'] - kelvin)  # converting default kelvin value to Celcius
        feels_like_temp = int(weather_info['main']['feels_like'] - kelvin)
        pressure = weather_info['main']['pressure']
        humidity = weather_info['main']['humidity']
        wind_speed = weather_info['wind']['speed'] * 3.6
        sunrise = weather_info['sys']['sunrise']
        sunset = weather_info['sys']['sunset']
        timezone = weather_info['timezone']
        cloudy = weather_info['clouds']['all']
        description = weather_info['weather'][0]['description']
 
        sunrise_time = time_format_for_location(sunrise + timezone)
        sunset_time = time_format_for_location(sunset + timezone)

# assigning Values to our weather varaible, to display as output
         
        weather = f"\nWeather of: {city_name}\nTemperature (Celsius): {temp}°\nFeels like (Celsius): {feels_like_temp}°\nPressure: {pressure} hPa\nHumidity: {humidity}%\nSunrise at {sunrise_time} and Sunset at {sunset_time}\nCloud: {cloudy}%\nInfo: {description}"
    else:
        weather = f"\n\tWeather for '{city_name}' not found!\n\tKindly Enter valid City Name !!" 
 
    tfield.insert(INSERT, weather)   # to insert or send value in our Text Field to display output

# ------------------------------Frontend part of code - Interface

headingLabel = Label(root, text = 'Welcome To The Weather App', bg = '#adebeb', fg = 'gray', font= 'Arial 18 bold')
headingLabel.pack()

photo = Image.open('weather.png')
resized_image = photo.resize((100,100), Image.ANTIALIAS)
photoLabel = ImageTk.PhotoImage(resized_image)
label1 = Label(image=photoLabel, bg = '#adebeb')
label1.image = photoLabel
label1.pack()

city_head = Label(root, text = 'Enter City Name', font = 'Arial 12 bold', bg = '#adebeb').pack(pady=10) # to generate label heading
 
inp_city = Entry(root, textvariable = city_value, bd = 2, width = 24, font = 'Arial 14 bold', fg = '#000099', cursor = 'cross').pack()

Button(root, command = showWeather, bd = 5, text = 'Check Weather', font = 'Arial 10 bold', bg = '#cc0000', fg = 'black', activebackground = '#ffcc99', padx=5, pady=5).pack(pady= 20)
     
# to show output
 
weather_now = Label(root, text = 'The Weather is: ', font = 'Arial 12 bold', bg = '#adebeb').pack(pady=10)

tfield = Text(root, width=46, height=10, bd = 2)
tfield.pack()
 
root.mainloop()