from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import RedirectView
from rest_framework.renderers import JSONRenderer
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
import json

# Import the API
from app import api
from app.api.serializers import UserSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


# define the catch all
def index(request):
    user_json = {}
    if request.user.is_authenticated():
        serialized = UserSerializer(request.user, context={'request': request})
        user_json = serialized.data

    return render_to_response('index.html', {
      'user': request.user,
      'user_json': JSONRenderer().render(user_json)
    })

@csrf_exempt
def register(request):
    data = json.loads(request.body)
    user = User(**data)
    user.set_password(data['password'])

    try:
        user.save()
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                request.user = user

                # Once we have logged the user in return the serialized response
                serializer = UserSerializer(request.user, context={'request': request})
                response = JSONResponse(serializer.data)
                response.status_code = 201
                return response

    except IntegrityError:
        pass

    response = HttpResponse()
    response.status_code = 409
    return response

def auth(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        uname, passwd = request.META['HTTP_AUTHORIZATION'].split(':')
        user = authenticate(username=uname, password=passwd)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.user = user

                # Once we have logged the user in return the serialized response
                serializer = UserSerializer(request.user, context={'request': request})
                return JSONResponse(serializer.data)

    # They did not provide basic authentication
    response = HttpResponse()
    response.status_code = 401
    return response


def vlogout(request):
    logout(request)
    return redirect('/')
