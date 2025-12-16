import socket
import requests.packages.urllib3.util.connection as urllib3_cn

from nasa.APOD import apod_send
from weather.weather import weather_send

def allowed_gai_family():
    return socket.AF_INET

urllib3_cn.allowed_gai_family = allowed_gai_family

def send_all():
    apod_send()
    weather_send()

def main():
    send_all()

if __name__ == '__main__':
    main()