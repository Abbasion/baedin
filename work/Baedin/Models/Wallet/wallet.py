import datetime
import json

from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from Baedin.Helpers.Users.Users import getUser_by_Id
from Baedin.Helpers.imgurlhelper.urlhelper import img_url_profile
from Baedin.Helpers.walletHelper.walletHelper import getWallet_by_Id, getAllWallet, getWallet_by_UserId
from Baedin_app.Models.Users.userSerializer import UserSerializer
from Baedin_app.Models.Wallet.wallet import Wallet



class WalletListUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):

        try:
            data = []

            wallet = getWallet_by_Id(pk)


            if (wallet is None):
                return Response({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            if wallet.userId.isDeleted ==True:
                return Response({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                data = model_to_dict(wallet)
                data['userId'] = UserSerializer(wallet.userId).data
                if (wallet.userId.profilePic):
                    data['userId']['profilePic'] = img_url_profile(wallet.userId.profilePic)

                return Response({"data": data, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        try:
            data = []

            wallets = getAllWallet()

            # if (user is None):
            #     return Response({"data": "user doesn't exists", "status": status.HTTP_404_NOT_FOUND},
            #                     status=status.HTTP_404_NOT_FOUND)
            for wallet in wallets:
                user = getUser_by_Id(wallet.userId)
                walletData = model_to_dict(wallet)
                walletData['userId'] = UserSerializer(wallet.userId).data
                if (wallet.userId.profilePic):
                    walletData['userId']['profilePic'] = img_url_profile(wallet.userId.profilePic)
                if wallet.userId.isDeleted == True:
                    continue
                data.append(walletData)

            return JsonResponse({"data": data, "Status": status.HTTP_200_OK})
        except Exception as ex:
            return JsonResponse({"data": str(ex), "Status": status.HTTP_403_FORBIDDEN})

    def post(self, request):
        try:
            d = request.data
            # d = json.loads(data)
            balance = 0
            if ('balance' in d.keys()):
                balance = d['balance']

            if 'Id' not in d.keys():
                return Response(
                    {"data": "Id is required id 0 for create"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            if 'userId' not in d.keys():
                return Response(
                    {"data": "userId is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            isDeleted = False
            if ('isDeleted' in d.keys()):
                isDeleted = d['isDeleted']
            user = getUser_by_Id(d['userId'])
            if (user is None):
                return Response({"data": "user doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            # user = request.user
            wallet = getWallet_by_UserId(d['userId'])
            id = d['Id'] == 0 or d['Id'] == None
            print(id)
            print(wallet)
            if (id and wallet is None):
                wallet = Wallet(
                    userId=user,
                    balance=balance,
                    isDeleted=isDeleted,

                )
                wallet.save()


                data = model_to_dict(wallet)
                data['userId'] = (UserSerializer(user)).data
                if (wallet.userId.profilePic):
                    data['userId']['profilePic'] = img_url_profile(wallet.userId.profilePic)

                return Response({"data": data, "status": status.HTTP_201_CREATED}, status=status.HTTP_200_OK)

            else:

                if ('balance' not in d.keys()):
                    return Response({"data": "Balance is required", "status": status.HTTP_404_NOT_FOUND},
                                    status=status.HTTP_404_NOT_FOUND)


                wallet.userId = user
                wallet.isDeleted = isDeleted
                wallet.balance = str(float(wallet.balance) + float(d['balance']))

                wallet.save()



            data = model_to_dict(wallet)
            data['userId'] = (UserSerializer(user)).data
            if (wallet.userId.profilePic):
                data['userId']['profilePic'] = img_url_profile(wallet.userId.profilePic)
            return Response({"data": data, "status": status.HTTP_201_CREATED}, status=status.HTTP_200_OK)
        except Exception as ex:
            # print(ex)
            return Response({"data": str(ex), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WalletsByUserIdUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            d = request.data
            if not d['balance']:
                return Response(
                    {"data": "Balance is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            if not d['userId']:
                return Response(
                    {"data": "UserId is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            if ('isSubtract' not in d.keys()):
                return Response(
                    {"data": "isSubtract is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            #     isSubtract = d['isSubtract']
            # else:



            wallet = getWallet_by_UserId(d['userId'])

            user = request.user
            if (wallet is None):
                return Response({"data": "wallet doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            if wallet.userId.isDeleted == True:
                return Response({"data": "User is deleted so Wallet doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                if (d['isSubtract'] == True):
                    if (float(wallet.balance) < float(d['balance'])):
                            return Response({"data": "you don't have enough money",
                                             "status": status.HTTP_400_BAD_REQUEST},
                                            status=status.HTTP_400_BAD_REQUEST)
                    elif(float(wallet.balance) - float(d['balance'])) >= 0:
                        wallet.balance = str(float(wallet.balance) - float(d['balance']))







                else:
                    wallet.balance = str(float(wallet.balance) + float(d['balance']))

                wallet.save()
                data = model_to_dict(wallet)
                data['userId'] = (UserSerializer(wallet.userId)).data

                if (wallet.userId.profilePic):
                    data['userId']['profilePic'] = img_url_profile(wallet.userId.profilePic)

                return Response({"data": data, "status": status.HTTP_201_CREATED}, status=status.HTTP_200_OK)
        except Exception as ex:
            # print(ex)
            return Response({"data": str(ex), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, pk, format=None):
        try:

            data = {}
            # if userId.isDeleted == False:
            # user = getUser_by_Id(pk)
            # if (user is None):

            wallet = getWallet_by_UserId(pk)

            if (wallet is None):
                return Response({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            if wallet.userId.isDeleted == True:
                return Response({"data": "wallet doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)

            walletData = model_to_dict(wallet)

            walletData['userId'] = UserSerializer(wallet.userId).data
            if (wallet.userId.profilePic):
                walletData['userId']['profilePic'] = img_url_profile(wallet.userId.profilePic)

            return Response({"data": walletData, "Status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "Status": status.HTTP_403_FORBIDDEN})