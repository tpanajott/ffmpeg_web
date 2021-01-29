FROM d2dyno/ffmpeg-docker

RUN apt update
RUN apt -y install python3 python3-pip

COPY FFMPEGWeb/ /FFMPEGWeb/

RUN pip3 install -r /FFMPEGWeb/requirements.txt

WORKDIR "/FFMPEGWeb/"
ENTRYPOINT ["/usr/bin/python3", "/FFMPEGWeb/manage.py", "runserver", "0.0.0.0:80"]