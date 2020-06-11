FROM python:3.8

RUN pip3 install aiohttp
RUN pip3 install httpx
RUN pip3 install opencv-python
RUN apt-get update
RUN apt-get install -y x11-xserver-utils
RUN apt-get install -y xauth
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y xorg --quiet
RUN apt-get install -y openbox
RUN apt-get install -y mesa-utils