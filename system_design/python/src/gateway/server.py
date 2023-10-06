import os, gridfs, pika, json

from flask import Flask, request
from flask_pymongo import PyMongo # mongo db

from auth import validate
from auth_svc import access
from storage import util

server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minicube.internal:27017/videos"

mongo = PyMongo(server) # interface wrap that will enable us to interact with Mongo DB

# we'll use MongoDB to store video and mp3 files

fs = gridfs.GirdFS(mongo.db) # Allows us to work with files of size above 16 MB 
# (MongoDB limits the size of files to avoid performance degradation)

# gridFS divides large files into different parts

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq")) # make connections synchronous with rabbitmq

# the rabbitmq string is referencing our rabbitmq host

channel = connection.channel()

# using a queue allows us asynchronous communication between the API gateway and the converting service

@server.route("/login", methods=["POST"])
def login():
    # log user in and assign token
    token, err = access.login(request)

    if err == None:
        return token
    else:
        return err
    
@server.route("/upload", methods=["POST"])
def upload():
    # validate user
    access, err = validate.token(request)

    access = json.loads(access) # convert JSON string to Python object (dictionary in our case)

    if access["admin"]:
        if len(request.files) != 1:
            return "exactly 1 file required", 400
        
        for _, file in request.files.items():
            err = util.upload(file, fs, channel, access)

            if err:
                return err
        
        return "success!", 200
    else:
        return "not authorized", 401