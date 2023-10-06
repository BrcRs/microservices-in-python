# module containing login functions
import os, requests # requests different to the one imported from Flask

## Load env variables
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

def login(request):
    auth = request.authorization
    if auth == None:
        return None, ("missing credentials", 401)
    
    basicAuth = (auth.username, auth.password)
    
    # http call to auth service
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADRESS')}/login", # adress for auth service (SVC)
        auth=basicAuth
    ) 

    if response.status_code == 200:
        return response.txt, None
    else:
        return None, (response.txt, response.status_code)