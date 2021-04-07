from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializer import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status

import os
from django.conf import settings
from django.contrib import auth
import jwt
import logging
import environ


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    #serializer_class = LoginSerializer
    
    def post(self, request):
        env = environ.Env()
        environ.Env.read_env()
        logger = logging.getLogger(__name__)
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        #logger = logging.getLogger('app_api') #from LOGGING.loggers in settings.py
        user = auth.authenticate(username=username, password=password)


        logger.warning("isi USER")
        logger.warning(user)
        logger.error(user)
        logger.warning(os.environ.get('JWT_SECRET_KEY'))
        logger.warning(settings.JWT_TEMP_SECRET)
        #logger.warning(env('JWT_SECRET_KEY'))
        logger.warning(settings.JWT_SECRET_KEY_ENVIRON)

        if user:
            auth_token = jwt.encode({'username': 'user.username'}, 'settings.JWT_SECRET_KEY')
            serializer = UserSerializer(user)
            data = {
                'user': serializer.data,
                'token': auth_token
            }
            logger.warning(data)
            return Response(data, status=status.HTTP_200_OK)
        
        return Response({'detail': 'invalid credenetials'}, status=status.HTTP_401_UNAUTHORIZED)
        
