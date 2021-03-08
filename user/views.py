from random import random, randint

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import Tel_optSerializer
from .models import Tel_opt
from .serializers import UserSerializer
from kavenegar import *


def kave_negar_token_send(receptor, token):
    f = open("/home/mehdi/Documents/kavenegar", 'r')
    API_KEY = f.read()
    f.close()

    try:
        api = KavenegarAPI(API_KEY)
        params = {
            'receptor': receptor,
            'template': 'your_template',
            'token': token
        }
        response = api.verify_lookup(params)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


@api_view(['POST'])
@permission_classes((AllowAny,))
def generate_otp(request):
    mobile = request.data.get('phone_number', None)
    opt = randint(10000, 99999)
    try:
        kave_negar_token_send(mobile, opt)
        data = {
            'phone_number': mobile,
            'opt': opt
        }
        ser = Tel_optSerializer(data=data)
        if ser.is_valid():
            ser.save()
            return Response(status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes((AllowAny,))
def verify_otp(request):
    opt = request.data.get('opt', None)
    phone_number = request.data.get('phone_number', None)
    # print(request.data.get('phone_number', None))
    # print(request.data.get('first_name', None))
    # print(request.data.get("last_name", None))
    # print(request.data.get("password", None))
    data = {
        'phone_number': request.data.get('phone_number', None),
        'first_name': request.data.get('first_name', None),
        'last_name': request.data.get("last_name", None),
        'password': request.data.get("password", None)
    }
    print(data)
    ser = UserSerializer(data=data)
    print(type(opt))
    if opt:
        try:
            tel = Tel_opt.objects.get(phone_number=phone_number)
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=status.HTTP_201_CREATED)

            else:
                return Response({'message': 'bad json'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'message': 'OTP is empty'}, status=status.HTTP_400_BAD_REQUEST)
