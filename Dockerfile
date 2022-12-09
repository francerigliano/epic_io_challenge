FROM python:latest
LABEL Maintainer="prueba"
WORKDIR /usr/app/src
RUN pip install numpy
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install opencv-contrib-python==3.4.18.65
COPY epic_io_funcion.py ./
COPY development_assets development_assets
CMD [ "python", "./epic_io_funcion.py"]