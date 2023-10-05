FROM python:3.10-slim-bullseye


# apt-get update && apt-get install python3-dev default-libmysqlclient-dev
# apt-get update && apt-get install default-libmysqlclient-dev && pip install --no-cache-dir --upgrade pip

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential default-libmysqlclient-dev \
    && pip install --no-cache-dir --upgrade pip

# RUN apt-get update \
#     && apt-get install -y --no-install-recommends --no-install-suggests \
#     build-essential python3-dev default-libmysqlclient-dev \
#     && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./docker_requirements.txt /app
# RUN pip install --no-cache-dir --requirement /app/docker_requirements.txt
RUN MYSQLCLIENT_CFLAGS="-I/usr/include/mysql" MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lmysqlclient" pip install --no-cache-dir --requirement /app/docker_requirements.txt
COPY . /app

EXPOSE 5000

CMD ["python3", "server.py"]

# when we build a docker image we build it on top of a base image which in our case is 
# python:3.10-slim-bullseye

# An image is like a filesystem snapshot
# in our example our base image is a snapshot of a filesystem containing all the 
# necessary dependencies to run our python application 

# each instruction in this file adds a new image layer to the previous one

# When a change is made, for example in requirements.txt, docker is smart and will not
# rebuild the first unaffected layers (and will use a cached version of the 
# layers) until the affected layer which will be rebuilt aswell as any layer coming after