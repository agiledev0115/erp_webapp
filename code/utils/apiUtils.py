from webbrowser import get
from rest_framework.authtoken.models import Token
import requests
from django.http import HttpResponse

# Get user token

def api_auth(user, content_type:str = None, asHeader:bool = False, only_token: bool= False):
    """
    get authorization token for a user, user header True to get authorization header for requests methods
    for json content type, add content_type = 'json'
    use user = request.user
    """
    token = Token.objects.get(user=user).key

    if only_token:
        return token

    if asHeader:
        requestHeader = {'Authorization':f"Token {token}"}
        
        if content_type is not None:
            if str.lower(content_type) == 'json':
                requestHeader.update({'Content-Type':'application/json'})
        return requestHeader

def api_get(url, request, render = None, post_content_type:str =None):


    try:
        apiGet = requests.get(url=url, headers=api_auth(user=request.user, asHeader=True, content_type=post_content_type))
        apiGet.raise_for_status()
        
        if render is not None:
            return render
        return apiGet

    except requests.exceptions.HTTPError as e:
        return HttpResponse(content=f"""<h1>Something went wrong</h1>
                                        <h1>URL: {url}</h1>
                                        <h2>CODE: {apiGet.status_code}  {apiGet.reason}</h2>
                                        <h2>{e.response.text}</h2>
                                        """)

def api_post(url, request, files= None, data= None, render = None, post_content_type:str =None):


    try:
        apiPost = requests.post(url=url, headers=api_auth(user=request.user, asHeader=True, content_type=post_content_type), data= data, files=files)
        apiPost.raise_for_status()
        
        if render is not None:
            return render
        return apiPost

    except requests.exceptions.HTTPError as e:
        return HttpResponse(content=f"""<h1>Something went wrong</h1>
                                        <h1>URL: {url}</h1>
                                        <h2>CODE: {apiPost.status_code}  {apiPost.reason}</h2>
                                        <h2>{e.response.text}</h2>
                                        """)

def api_patch(url, request, data, render = None, post_content_type:str =None):


    try:
        apiPatch = requests.patch(url=url, headers=api_auth(user=request.user, asHeader=True, content_type=post_content_type), data= data)
        apiPatch.raise_for_status()
        
        if render is not None:
            return render
        return apiPatch

    except requests.exceptions.HTTPError as e:
        return HttpResponse(content=f"""<h1>Something went wrong</h1>
                                        <h1>URL: {url}</h1>
                                        <h2>CODE: {apiPatch.status_code}  {apiPatch.reason}</h2>
                                        <h2>{e.response.text}</h2>
                                        """)


def api_delete(request, url):

    try:
        apiDelete = requests.delete(url=url, headers=api_auth(user=request.user, asHeader=True))
    
    except requests.exceptions.HTTPError as e:
        return HttpResponse(content=f"""<h1>Something went wrong</h1>
                                        <h1>URL: {url}</h1>
                                        <h2>CODE: {apiDelete.status_code}  {apiDelete.reason}</h2>
                                        <h2>{e.response.text}</h2>
                                        """)