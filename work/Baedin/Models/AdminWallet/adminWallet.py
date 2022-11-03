import datetime

from django.forms import model_to_dict
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json

from Baedin.Helpers.AdminWallet.AdminWalletHelper import Admin_Wallet_by_Id, get_admin_wallet_Id
from Baedin.Helpers.Users.Users import getUser_by_Id, getAdmin
from Baedin_app.Models.AdminWallet.adminWallet import AdminWallet
from Baedin_app.Models.Users.userSerializer import UserSerializer





class AdminWalletListUpdateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            data = request.data
            dic = json.dumps(data)
            dic = json.loads(dic)
            wallet = Admin_Wallet_by_Id()
            # notification_to = getReceive_by_Phonenumber(dic['receiverPhone'])
            # user = getUser_by_Id(dic['userId'])
            isDeleted = False
            if ('isDeleted' in dic.keys()):
                isDeleted = dic['isDeleted']
            if ('balance' in dic.keys()):
                balance = dic['balance']
            else:
                return Response(
                    {"data": "Balance is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            if wallet is None:
                AD_wallet = AdminWallet(

                    balance=balance,
                    isDeleted=isDeleted,

                )
                AD_wallet.save()

                data = model_to_dict(AD_wallet)

                return Response({"data": data, "status": status.HTTP_201_CREATED}, status=status.HTTP_200_OK)

            else:

                wallet.balance =  str(float( wallet.balance ) + float(balance))
                wallet.isDeleted = isDeleted
                wallet.save()

                data = model_to_dict(wallet)

                return Response({"data": data, "status": status.HTTP_201_CREATED}, status=status.HTTP_200_OK)
        except Exception as ex:
            # print(ex)
            return Response({"data": str(ex), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request, *args, **kwargs):
        try:
            dic = request.data
            wallet = Admin_Wallet_by_Id()
            if ('balance' in dic.keys()):
                balance = dic['balance']
            else:
                return Response(
                    {"data": "Balance is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            isDeleted = False
            if ('isDeleted' in dic.keys()):
                isDeleted = dic['isDeleted']
            if (wallet is None):
                return Response({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                wallet.balance = str(float(wallet.balance) - float(balance))
                wallet.isDeleted = isDeleted
                wallet.save()
                data = model_to_dict(wallet)




                return Response({"data": data, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, pk):
        try:
            data = []
            wallet = get_admin_wallet_Id(pk)
            if(wallet is None):
                return Response({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},status=status.HTTP_404_NOT_FOUND)
            else:

                data = model_to_dict(wallet)


            return Response({"data": data, "status": status.HTTP_200_OK},status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_500_INTERNAL_SERVER_ERROR},status=status.HTTP_500_INTERNAL_SERVER_ERROR)