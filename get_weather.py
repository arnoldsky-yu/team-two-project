import requests
import json
url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0003-001?Authorization=CWA-E0209D98-7FF4-4B91-BAC6-8473D7A01C11&limit=10&offset=0&format=JSON&StationId=466920,467660,467490,467441&WeatherElement=&GeoInfo="

def get_weather():
    '''
    This function is used to get the weather information from the url
    input: None
    output: weather_info

    weather_info: list of dictionary, data_example:
    [{'Station': '臺中', 'Weather': '晴', 'Temperature': 28.3}, 
    {'Station': '高雄', 'Weather': '陰', 'Temperature': 26.6}, 
    {'Station': '臺東', 'Weather': '陰', 'Temperature': 29.2}, 
    {'Station': '臺北', 'Weather': '晴', 'Temperature': 30.1}]
    '''
    data = requests.get(url)
    data_json = data.json()


    stations = data_json["records"]["Station"]
    weather_info = []
    # store by list and dictionary

    for station in stations:
        station_name = station["StationName"]
        weather = station["WeatherElement"]["Weather"]
        AirTemperature = station["WeatherElement"]["AirTemperature"]
        weather_info.append({"Station": station_name, "Weather": weather, "Temperature": AirTemperature})


    return weather_info