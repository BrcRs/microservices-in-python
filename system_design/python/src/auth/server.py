import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

## Load env variables
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

server = Flask(__name__)

mysql = MySQL(server)

# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST") # retrieve env var
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER") # retrieve env var
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD") # retrieve env var
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB") # retrieve env var
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT") # retrieve env var

# class 

@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization # provide credentials for basic auth scheme
    # auth.username
    # auth.password
    if auth == None:
        return "missing credentials", 401
    
    # check db for username and pswrd
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username,)
    )
    # check existence of user
    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]
        # check password
        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        # the user doesn't exist
        return "invalid credentials", 401

@server.route("/validate", method=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if encoded_jwt == None:
        return "missing credentials", 401

    # Authorization: Bearer <token>
    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithm=["HS256"]
        )
    except:
        return "not authorized", 403
    return decoded, 200


def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz, # permission for admin
        },
        secret,
        algorithm="HS256",
    )

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)