FROM ubuntu:22.04 

#no-cache since the cache would make the image bigger than needed.
RUN apt-get update && apt-get install --no-install-recommends -y \ 
python3-setuptools \
python3 \ 
python3-pip \
tesseract-ocr \
tesseract-ocr-deu \
libsm6 \
libxext6 \
libglu1 \
ffmpeg \
&& rm -rf /var/lib/apt/lists/*

 #create the folder app
ADD requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
WORKDIR /app
ADD imagetopdfandtxt /app/imagetopdfandtxt
ADD tests /app/tests/

#Command used, despite specified command.
#ENTRYPOINT python3 run.py

#Use this as default command, if no command has been specified in docker run ...
CMD python3 -m imagetopdfandtxt.main -f convert
