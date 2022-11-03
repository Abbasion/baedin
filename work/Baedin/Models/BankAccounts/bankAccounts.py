from django.forms import model_to_dict
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Baedin.Helpers.BankAccountsHelper.bankAccountsHelper import get_Account_By_Id, get_All_Bank_Accounts, \
    get_All_Banks_Accounts_by_UserId, get_Account_By_Name
from Baedin.Helpers.Users.Users import getUser_by_Id
from Baedin.Helpers.imgurlhelper.urlhelper import img_url_profile, img_url
from Baedin.settings import IMG_URL
from Baedin_app.Models.BankAccounts.bankAccounts import BankAccounts
from Baedin_app.Models.Users.userSerializer import UserSerializer


class BankAccountCreate(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            d = request.data
            # d = json.loads(data)
            if 'Id' not in d.keys():
                return Response(
                    {"data": "Id is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


            user = request.user
            if (user is None):
                return Response({"data": "user doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            isDeleted =False
            if ('isDeleted' in d.keys()):
                isDeleted = d['isDeleted']



            if (d['Id'] == 0 or d['Id'] == None):
                if ('bank_name' in d.keys()):
                    bank_name = d['bank_name']
                else:
                    return Response(
                        {"data": "Bank Name is required"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
                acc = get_Account_By_Name(d['bank_name'])
                if acc and isDeleted == False:
                    return Response(
                        {"data": "Account with this Name already exists",
                         "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

                if ('account_number' in d.keys()):
                    account_number = d['account_number']
                else:
                    return Response(
                        {"data": "Account Number is required"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )


                account = BankAccounts(
                    userId=user,
                    bank_name=bank_name,
                    account_number=account_number,
                    isDeleted=isDeleted

                    )
                account.save()

                data = model_to_dict(account)
                data['userId'] = (UserSerializer(account.userId)).data
                if (account.userId.profilePic):
                    data['userId']['profilePic'] = str(IMG_URL) + "/Baedin/uploads/" + str(account.userId.profilePic)
                return Response({"data": data, "status": status.HTTP_201_CREATED}, status=status.HTTP_200_OK)
            else:
                account = BankAccounts.objects.get(pk=d['Id'])
                if (account is None):
                    return Response({"data": "Bank Account doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                    status=status.HTTP_404_NOT_FOUND)
                if 'isDeleted' in d.keys():
                    account.isDeleted = d['isDeleted']
                if 'bank_name' in d.keys():
                    account.bank_name = d['bank_name']
                if 'account_number' in d.keys():
                    account.account_number = d['account_number']
                account.save()

                data = model_to_dict(account)
                data['userId'] = (UserSerializer(account.userId)).data
                if (account.userId.profilePic):
                    data['userId']['profilePic'] = str(IMG_URL) + "/Baedin/uploads/" + str(account.userId.profilePic)


            return Response({"data": data, "status": status.HTTP_201_CREATED}, status=status.HTTP_200_OK)

        except Exception as ex:
            return Response({"data": str(ex), "Status": status.HTTP_403_FORBIDDEN})

    def put(self, request, pk, format=None):
        try:
            data = []
            account = get_Account_By_Id(pk)
            if (account is None):
                return Response({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                data = model_to_dict(account)
                data['userId'] = (UserSerializer(account.userId)).data
                if (account.userId.profilePic):
                    data['userId']['profilePic'] = img_url_profile(account.userId.profilePic)
                return Response({"data": data, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        try:

            data = []

            accounts = get_All_Bank_Accounts()
            if (accounts is None):
                return Response({"data": "Cards doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            for account in accounts:
                acc_data = model_to_dict(account)
                acc_data['userId'] = UserSerializer(account.userId).data
                if (account.userId.profilePic):
                    acc_data['userId']['profilePic'] = img_url_profile(account.userId.profilePic)
                data.append(acc_data)

            return Response({"data": data, "Status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "Status": status.HTTP_403_FORBIDDEN})

    def patch(self, request, pk, format=None):
        try:

            data = []
            categories = get_All_Banks_Accounts_by_UserId(pk)
            for category in categories:
                cat_Data = model_to_dict(category)
                cat_Data['userId'] = UserSerializer(category.userId).data
                if (category.userId.profilePic):
                    cat_Data['userId']['profilePic'] = img_url(category.userId.profilePic)

                data.append(cat_Data)

            return Response({"data": data, "Status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "Status": status.HTTP_403_FORBIDDEN},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)