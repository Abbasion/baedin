import datetime
import json
import base64
import math
import os
import shutil
# from urllib.request import urlopen
# from PIL import Image

import jwt
from django.contrib.auth import authenticate, user_logged_in
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenViewBase

from Baedin import settings
from Baedin.Helpers.Auth.token import get_token_for_user, verify_token
from Baedin.Helpers.Users.Users import getUsers, getAdmin, getUser_by_Phone, getUser_by_Mail
from Baedin.Helpers.Users import Users
from Baedin.Helpers.walletHelper.walletHelper import getWallet_by_UserId
from Baedin.settings import IMG_URL


from Baedin_app.Models.Users.users import User as user
from Baedin_app.Models.Users.userSerializer import UserSerializer



@csrf_exempt
@require_http_methods(["POST"])
def Login(request):
    try:
        x = request.body

        # print(x)
        # x = json.dumps(x)

        x = json.loads(x)
        # print(x)
        if ('password' in x.keys()):
            if not x['password']:
                return JsonResponse(
                    {"data": "Password is required", "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            else:
                if (x['password']):
                    password = x['password']
        # Email=''
        # if ('Email' in x.keys()):
        #     if not Email:
        #         return JsonResponse(
        #             {"data": "Email is required", "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
        #             status=status.HTTP_500_INTERNAL_SERVER_ERROR
        #         )
        #     else:
        #         if (x['Email']):
        #             Email = x['Email']

        email = x['Email']

        password = password
        # print(email)
        # print(password)

        # password = PasswordManager.encrypt(password)

        user = authenticate(Email=email, password=password)
        # print(user,"User")

        if user and user.isDeleted == False and user.isActive == True:
            try:
                payload = get_token_for_user(user)
                # token = jwt.encode(payload, settings.SECRET_KEY)

                user_details = {}
                user_details['Token'] = payload['access']

                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                user_details["user"] = UserSerializer(user).data
                newData = user_details["user"]
                if (newData['profilePic'] and user.isSocial == False):
                    pp = str(IMG_URL) + "/Baedin/uploads/" + str(newData['profilePic'])
                    newData['profilePic'] = pp

                data = newData

                user_details['user'] = data

                return JsonResponse({"data""": user_details, "status": status.HTTP_200_OK})
            except Exception as e:

                return Response({"data": str(e), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return JsonResponse({"data": res, "status": status.HTTP_403_FORBIDDEN})

    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response({"data": str(res), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateUserAPIView(CreateAPIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)

    def post(self, request):

        try:
            data = request.data
            dic = json.dumps(data)
            dic = json.loads(dic)
            if ('Id' not in dic.keys()):
                return Response(
                    {"data": " Id is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            if ('password' in dic.keys()):
                if not dic['password']:
                    return Response(
                        {"data": "Password is required", "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                else:
                    if (dic['password']):
                        password = dic['password']

            profilePic = ""


            if ('profilePic' in dic.keys() and dic['isSocial'] == True):
                profilePic = dic['profilePic']

            language = ""
            if ('language' in dic.keys()):
                language = dic['language']
            country = ""
            if ('country' in dic.keys()):
                country = dic['country']
            RoleType = 2
            RoleName = "User"
            if ('RoleType' in dic.keys()):
                if (dic['RoleType'] == 0):
                    RoleName = 'Admin'
                    RoleType = 0
                elif (dic['RoleType'] == 1):
                    RoleName = 'Partner'
                    RoleType = 1

                elif (dic['RoleType'] == 2):
                    RoleName = 'User'
                    RoleType = 2

            isDeleted = False
            if ('isDeleted' in dic.keys()):
                isDeleted = dic['isDeleted']

            address = ""
            if ('address' in dic.keys()):
                address = dic['address']
            isVerified = ""
            if ('isVerified' in dic.keys()):
                isVerified = dic['isVerified']
            isActive = ""
            if ('isActive' in dic.keys()):
                isActive = dic['isActive']

            if (dic['Id'] == 0 or dic['Id'] is None):
                isSocial = ''
                if ('isSocial' in dic.keys()):
                    isSocial = dic['isSocial']
                else:
                    return Response(
                        {"data": "isSocial is required", "status": status.HTTP_500_INTERNAL_SERVER_ERROR },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )


                if ('password' in dic.keys()):
                    if not dic['password'] :
                        return Response(
                            {"data": "Password cannot be empty", "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
                    else:
                        if(dic['password']):
                            password = dic['password']
                else:
                    return Response(
                        {"data": "password is required", "status": status.HTTP_500_INTERNAL_SERVER_ERROR },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                UserName = ""
                if ('UserName' in dic.keys()):
                    UserName = dic['UserName']
                else:
                    return Response(
                        {"data": "UserName is required", "status": status.HTTP_500_INTERNAL_SERVER_ERROR },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                Email = ""
                if ('Email' in dic.keys()):
                    Email = dic['Email']
                else:
                    return Response(
                        {"data": "Email is required", "status": status.HTTP_500_INTERNAL_SERVER_ERROR },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

                PhoneNumber = ""
                if ('PhoneNumber' in dic.keys()):
                    PhoneNumber = dic['PhoneNumber']
                else:
                    return Response(
                        {"data": "Phone Number is required", "status": status.HTTP_500_INTERNAL_SERVER_ERROR },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                checkUser = user.objects.filter(Email=dic["Email"], isDeleted=False).exists()
                checkphone = user.objects.filter(PhoneNumber=dic["PhoneNumber"], isDeleted=False).exists()

                if checkUser and isSocial == False:
                    return Response(
                        {"data": "User with this Email already exists", "status": status.HTTP_500_INTERNAL_SERVER_ERROR },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

                elif checkphone and dic['isSocial'] == False:
                    return Response(
                        {"data": "User with this Phone Number already exists", "status": status.HTTP_500_INTERNAL_SERVER_ERROR },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

                elif checkUser  and dic['isSocial'] == True:
                    if not dic['password'] :
                        return Response(
                        {"data": "Password is required", "status": status.HTTP_500_INTERNAL_SERVER_ERROR },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                    _user = user.objects.get(Email=Email)
                    # _user.profilePic = profilePic
                    _user.isDeleted = isDeleted
                    _user.UserName = UserName
                    _user.PhoneNumber = PhoneNumber
                    _user.Country = country
                    _user.RoleType = RoleType
                    _user.RoleName = RoleName
                    _user.address = address
                    _user.isSocial = isSocial
                    _user.isVerified = isVerified
                    _user.isActive = isActive
                    _user.language = language
                    _user.set_password(password)
                    if ("profilePic" in dic.keys()):
                        if not dic['profilePic']:
                            return Response(
                                {"data": "Please upload you profilePic", "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                        if (isinstance(dic['profilePic'], str) and dic['isSocial'] == True):
                            _user.profilePic = str(dic['profilePic'])
                        elif (isinstance(dic['profilePic'], dict) and dic['isSocial'] == True):
                            return Response(
                                {"data": "you are trying to login with social Account please provide the link your image", "status": status.HTTP_500_INTERNAL_SERVER_ERROR },
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                            )

                    _user.profilePic = profilePic
                    _user.save()
                    serializer = UserSerializer(_user)
                    data = serializer.data
                    if (_user.profilePic and _user.isSocial == False):
                        pp = str(IMG_URL) + "/Baedin/uploads/" + str(_user.profilePic)
                        data['profilePic'] = pp

                    return Response(data, status=status.HTTP_201_CREATED)

                else:
                    if(checkphone):
                        return Response(
                            {"data": "User with this Phone Number already exists",
                             "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
                    else:

                        _user = user(UserName=UserName, Email=Email, PhoneNumber=PhoneNumber,

                                     Country=country, RoleType=RoleType, RoleName=RoleName,
                                     profilePic=profilePic, address=address,language=language,

                                     Creation_Time=datetime.datetime.now(), Deletion_Time=None, isDeleted=False,
                                     isVerified=isVerified, isSocial=isSocial,
                                     isActive=isActive,
                                     )
                        _user.set_password(password)
                        _user.save()

                        serializer = UserSerializer(_user)

                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                # try:
                #     userId = urlsafe_base64_encode(force_bytes(_user.pk))
                #     token = account_activation_token.make_token(_user)
                #     url = settings.client+"/activate/"+userId+"/"+token
                #     txt = "Please click on the link to confirm your registration, <br/>"+url+" <br/> <br/> OR    \
                #      <a href="+url+" target='_blank' style='background:#2088C9;border-radius:15px; padding:10px;text-decoration:none;margin:5px auto; color:white'>Activate</a>\
                #         <br/><br/>If you think, it's not you, then just ignore this email"
                #     t = threading.Thread(target= EmailHelper.send_Mail,
                #                          args=("Activate your account",txt,_user.UserName,_user.Email))
                #     t.setDaemon(True)
                #     t.start()
                #     # EmailHelper.send_Mail("Activate your account",txt,_user.UserName,_user.Email)
                # except:
                #     pass

            else:
                _user = user.objects.get(pk=dic['Id'])

                if ("password" in dic.keys()):
                    isActive = False
                    isDeleted = False

                    _user.set_password(dic["password"])
                    if (dic['isActive'] == True):
                        isActive = True
                        isDeleted = False
                    if (dic['isDeleted'] == True):
                        isActive = False
                        isDeleted = True

                    if ("address" in dic.keys()):
                        _user.address = dic['address']
                    if ("language" in dic.keys()):
                        _user.language = dic['language']
                    if ("country" in dic.keys()):
                        _user.Country = dic['country']
                    if ("UserName" in dic.keys()):
                        _user.UserName = dic['UserName']
                    if ("isSocial" in dic.keys()):
                        _user.isSocial = dic['isSocial']
                    # if ('UserName' in dic.keys()):
                    #     _user.UserName = dic['UserName']
                    # else:
                    #     return Response(
                    #         {"data": "UserName is required"},
                    #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    #     )
                    email = _user.Email
                    if ('Email' in dic.keys()):
                        _user.Email = dic['Email']
                    else:
                        _user.Email=email
                    # else:
                    #     return Response(
                    #         {"data": "Email is required"},
                    #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    #     )

                    PhoneNumber = _user.PhoneNumber
                    if ('PhoneNumber' in dic.keys()):
                        _user.PhoneNumber = dic['PhoneNumber']
                    else:
                        _user.PhoneNumber = PhoneNumber
                    # else:
                    #     return Response(
                    #         {"data": "Phone Number is required"},
                    #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    #     )

                    # checkUser = user.objects.filter(Email=dic["Email"], isDeleted=False).exists()
                    # checkphone = user.objects.filter(PhoneNumber=dic["PhoneNumber"], isDeleted=False).exists()
                    # if checkUser and "Email" in dic.keys():
                    #     return Response(
                    #         {"data": "User with this Email already exists"},
                    #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    #     )
                    # else:
                    #         _user.Email = dic['Email']
                    # if checkphone and "PhoneNumber" in dic.keys():
                    #     return Response(
                    #         {"data": "User with this Phone Number already exists"},
                    #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    #     )
                    # else:
                    #     _user.PhoneNumber = dic['PhoneNumber']

                    if ("profilePic" in dic.keys()):
                        if not dic['profilePic']:
                            return Response(
                                {"data": "Please upload you profilePic", "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST
                            )

                        if (isinstance(dic['profilePic'], str) and dic['isSocial'] == True):
                            _user.profilePic = str(dic['profilePic'])
                        elif (isinstance(dic['profilePic'], dict)and dic['isSocial'] == True):
                            return Response(
                                {"data": "you are not login with social Account please provide the link your image", "status": status.HTTP_500_INTERNAL_SERVER_ERROR },
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                            )
                        elif (isinstance(dic['profilePic'], str) and dic['isSocial'] == False):
                            return Response(
                                {"data": "you are not login with social account please upload your profile picture", "status": status.HTTP_500_INTERNAL_SERVER_ERROR },
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                            )

                        elif (isinstance(dic['profilePic'], dict)):
                          if ("fileName" in dic["profilePic"].keys()):
                            url = dic['profilePic']["filePath"]
                            url = url.split(",")
                            filedata = base64.b64decode(url[1])
                            name = str(math.trunc(datetime.datetime.now().timestamp())) + "_" + dic['profilePic'][
                                'fileName']
                            filename = str(settings.BASE_DIR) + r"\Baedin/uploads\\" + name
                            with open(filename, 'wb') as f:
                                f.write(filedata)
                                f.close()

                                if (_user.profilePic):
                                    if os.path.exists(str(settings.BASE_DIR) + r"\Baedin/uploads\\" + _user.profilePic):
                                        os.remove(str(settings.BASE_DIR) + r"\Baedin/uploads\\" + _user.profilePic)

                                _user.profilePic = name
                    # _user.profilePic = profilePic

                    # if ('RoleType' in dic.keys()):
                    #     if (dic['RoleType'] == 0):
                    #         _user.RoleName = 'Admin'
                    #         _user.RoleType = 0
                    #     elif (dic['RoleType'] == 1):
                    #         _user.RoleName = 'Partner'
                    #         _user.RoleType = 1
                    #
                    #     elif (dic['RoleType'] == 2):
                    #         _user.RoleName = 'User'
                    #         _user.RoleType = 2

                    _user.isActive = isActive
                    _user.isSocial = dic["isSocial"]
                    _user.address = dic["address"]
                    _user.isDeleted = isDeleted
                    _user.set_password(dic['password'])


                    _user.save()
                    serializer = UserSerializer(_user)
                    newData = serializer.data
                    if (_user.profilePic and _user.isSocial == False):
                        pp = str(IMG_URL) + "/Baedin/uploads/" + str(_user.profilePic)
                        newData['profilePic'] = pp
                    # elif(_user.profilePic is dict and _user.isSocial == True):
                    #     pp = str(IMG_URL) + "/Baedin/uploads/" + str(_user.profilePic)
                    #     newData['profilePic'] = pp
                    else:
                        pass
                    return Response({"data": newData, "status": 201}, status=status.HTTP_201_CREATED)


                else:
                    # _user = user.objects.get(pk=dic['Id'])

                    isActive = False
                    isDeleted = False

                    if (dic['isActive'] == True):
                        isActive = True
                        isDeleted = False
                    if (dic['isDeleted'] == True):
                        isActive = False
                        isDeleted = True
                    if ("address" in dic.keys()):
                        _user.address = dic['address']
                    if ("language" in dic.keys()):
                        _user.language = dic['language']
                    if ("country" in dic.keys()):
                        _user.Country = dic['country']
                    if ("UserName" in dic.keys()):
                        _user.UserName = dic['UserName']
                    if ("Email" in dic.keys()):
                        _user.Email = dic['Email']
                    isSocial = ''
                    if ('isSocial' in dic.keys()):
                        _user.isSocial = dic['isSocial']


                    if ("profilePic" in dic.keys()):
                        if not dic['profilePic']:
                            return Response(
                                {"data": "Please upload you profilePic", "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST
                            )

                        if (isinstance(dic['profilePic'],str) and dic['isSocial'] == True):
                            _user.profilePic = str(dic['profilePic'])
                        elif (isinstance(dic['profilePic'],dict) and dic['isSocial'] == True):
                            return Response(
                                {"data": "you are trying to login with social accounts please provide link of profille picture", "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                        elif (isinstance(dic['profilePic'], str)and dic['isSocial'] == False):
                            return Response(
                                {"data": "you are not login with social account please upload your profile picture", "status": status.HTTP_500_INTERNAL_SERVER_ERROR },
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                            )
                        elif (isinstance(dic['profilePic'], dict)):
                            if ("fileName" in dic["profilePic"].keys()):
                                url = dic['profilePic']["filePath"]
                                url = url.split(",")
                                filedata = base64.b64decode(url[1])
                                name = str(math.trunc(datetime.datetime.now().timestamp())) + "_" + dic['profilePic'][
                                    'fileName']
                                filename = str(settings.BASE_DIR) + r"\Baedin/uploads\\" + name
                                with open(filename, 'wb') as f:
                                    f.write(filedata)
                                    f.close()
                                    # _user = user.objects.get(pk=dic['Id'])
                                    if (_user.profilePic):
                                        if os.path.exists(
                                                str(settings.BASE_DIR) + r"\Baedin/uploads\\" + _user.profilePic):
                                            os.remove(str(settings.BASE_DIR) + r"\Baedin/uploads\\" + _user.profilePic)
                                            # from urllib.request import urlopen
                                            # url='http://localhost:8001/Baedin/uploads/'+filename
                                            # response = urlopen(url)
                                    _user.profilePic = name
                                    # _user.save()

                    # if ('RoleType' in dic.keys()):
                    #     if (dic['RoleType'] == 0):
                    #         _user.RoleName = 'Admin'
                    #         _user.RoleType = 0
                    #     elif (dic['RoleType'] == 1):
                    #         _user.RoleName = 'Partner'
                    #         _user.RoleType = 1
                    #
                    #     elif (dic['RoleType'] == 2):
                    #         _user.RoleName = 'User'
                    #         _user.RoleType = 2
                    _user.isActive = isActive
                    _user.address = dic["address"]
                    _user.isSocial = dic["isSocial"]
                    _user.isDeleted = isDeleted

                    _user.save()
                    serializer = UserSerializer(_user)
                    newData = serializer.data
                    if (_user.profilePic and _user.isSocial == False):
                        pp = str(IMG_URL) + "/Baedin/uploads/" + str(_user.profilePic)
                        newData['profilePic'] = pp

                    return Response({"data": newData, "status": 201}, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"data": str(ex), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class TokenVerify(TokenViewBase):
    # permission_classes = (IsAuthenticated,)
    serializer_class = TokenObtainPairSerializer

    def post(self, request):
        return verify_token(request)



class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        try:
            # serializer to handle turning our `User` object into something that
            # can be JSONified and sent to the client.
            # print(request.user)
            users = getUsers()
            data = []
            for user in users:
                serializer = self.serializer_class(user)
                newData = serializer.data
                if (user.profilePic and user.isSocial == False):
                    pp = str(IMG_URL) + "/Baedin/uploads/" + str(user.profilePic)
                    newData['profilePic'] = pp
                data.append(newData)

            # print(serializer.data)
            return Response({"data": data, "status": 200}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, format=None):
        try:
            user = Users.getUser_by_Id(pk)
            if (user is None):
                return Response({"data": "user doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            # serializer_data = request.data.get('user', {})
            serializer = self.serializer_class(user)
            newData = serializer.data
            if (user.profilePic and user.isSocial == False):
                pp = str(IMG_URL) + "/Baedin/uploads/" + str(user.profilePic)
                newData['profilePic'] = pp

            return Response(newData, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self,request, *args, **kwargs):
        try:
            # serializer to handle turning our `User` object into something that
            # can be JSONified and sent to the client.
            # print(request.user)
            d = request.data
            if ('Email' in d.keys()):
                Email = d['Email']
            else:
                return Response(
                    {"data": "Email is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            user = getUser_by_Mail(d['Email'])
            if user is None:
                return Response({"data": "User doesn't exists", "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.serializer_class(user)
            newData = serializer.data
            if (user.profilePic and user.isSocial == False):
                pp = str(IMG_URL) + "/Baedin/uploads/" + str(user.profilePic)
                newData['profilePic'] = pp

            # print(serializer.data)
            return Response({"data": newData, "status": 200}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self,request, *args, **kwargs):
        try:
            # serializer to handle turning our `User` object into something that
            # can be JSONified and sent to the client.
            # print(request.user)
            d = request.data
            if ('PhoneNumber' in d.keys()):
                PhoneNumber = d['PhoneNumber']
            else:
                return Response(
                    {"data": "PhoneNumber is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            user = getUser_by_Phone(d['PhoneNumber'])
            if user is None:
                return Response({"data": "User doesn't exists", "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.serializer_class(user)
            newData = serializer.data
            if (user.profilePic and user.isSocial == False):
                pp = str(IMG_URL) + "/Baedin/uploads/" + str(user.profilePic)
                newData['profilePic'] = pp

            # print(serializer.data)
            return Response({"data": newData, "status": 200}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class AdminRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        try:
            # serializer to handle turning our `User` object into something that
            # can be JSONified and sent to the client.
            # print(request.user)
            users = getAdmin()
            data = []
            for user in users:
                serializer = self.serializer_class(user)
                newData = serializer.data
                if (user.profilePic and user.isSocial == False):
                    pp = str(IMG_URL) + "/Baedin/uploads/" + str(user.profilePic)
                    newData['profilePic'] = pp
                data.append(newData)

            # print(serializer.data)
            return Response({"data": data, "status": 200}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)