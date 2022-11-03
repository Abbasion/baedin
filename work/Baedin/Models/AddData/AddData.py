import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Baedin_app.Models.AdminWallet.adminWallet import AdminWallet
from Baedin_app.Models.Users.users import User


@csrf_exempt

def addData(request):
    user = User(UserName="Baedin Admin", Email='adnanameer71119@gmail.com', RoleType=0,RoleName="Admin",
                     Creation_Time=datetime.datetime.now(),PhoneNumber="03121212990",Country='Pakistan',address='',
                     Deletion_Time=None, isDeleted=False, isActive=True)
    user.set_password('Admin@123')
    user.save()
    wallet = AdminWallet(balance=0)
    wallet.save()



    return JsonResponse({"msg":"Success"})