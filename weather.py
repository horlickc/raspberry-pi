import pywapi

location = "hong kong"

weather_lookup = pywapi.get_location_ids(location)

for n in weather_lookup:
    location_id = n

weather_r = pywapi.get_weather_from_weather_com(location_id)

temperature = weather_r['current_conditions']['temperature']
humidity = weather_r['current_conditions']['humidity']

print(temperature)
print(humidity)