from janus.janus import DataMessage, Attribute

class WeatherData (object):
    def __init__(self, hpa, temp, humidity):
        self.hpa = hpa
        self.temp = temp
        self.humidity = humidity


class WeatherDataMessage(DataMessage):
    hpa = Attribute(value_type=float,name="hpa",mapping="hpa")
    temp = Attribute(value_type=float,name="temp",mapping="temp")
    humidity = Attribute(value_type=float,name="humidity",mapping="humidity")
