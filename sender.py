from weather_data import WeatherData, WeatherDataMessage
from janus.janus import JsonApiMessage
import json, urllib2, serial
from config import APIKEY


#start

#read serial
def checkData(data):
    try:
        print "Test"
        val = data['temp']
        val = data['humidity']
        val = data['hPa']
        return True
    except Exception:
        return False

try:
    print "Connecting ..."
    arduino = serial.Serial('/dev/ttyACM0', 9600)
    time.sleep(2)

    print "Reading ..."

    success = False
    i = 0

    while(success == False and i < 100):
        response = arduino.readline(None)

        try:
            readValue = json.loads(response)

            if checkData(readValue):
                print "ok"
                weather_data = WeatherData(readValue["hPa"], readValue["temp"], readValue["humidity"])
                recorderLog(0,"Data written.")
                success = True

        except Exception, e:
            print "Error reading from arduino: " + response + " - " +  str(e)

        i = i+1

except Exception, e:
    print"Error while reading from arduino: " + str(e)



#is valid
#raw_weather_data = {"hPa": 959.11, "temp": 28.5, "humidity": 34.8}
#weather_data = WeatherData(raw_weather_data["hPa"], raw_weather_data["temp"], raw_weather_data["humidity"])

msg = json.dumps(JsonApiMessage(data = WeatherDataMessage.from_object(weather_data, WeatherDataMessage)).to_json())


#send
url = 'https://receiver-service-dot-salendron-go.appspot.com'

req = urllib2.Request(url)
req.add_header('Content-type', "application/vnd.api+json")
req.add_header('User-Agent', "Wetterhaeuschen")
req.add_header('Accept', "application/vnd.api+json")
req.add_header('Authorization', APIKEY)

resp = urllib2.urlopen(req,msg)

print resp.code
print resp.read()
