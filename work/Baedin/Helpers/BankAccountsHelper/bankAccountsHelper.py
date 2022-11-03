from Baedin_app.Models.BankAccounts.bankAccounts import BankAccounts


def get_Account_By_Id(Id):
    try:
        account=BankAccounts.objects.select_related("userId").get(isDeleted=False,pk=Id)
        return account
    except:
        return None

def get_All_Bank_Accounts():
    try:
        list =BankAccounts.objects.select_related("userId").filter(isDeleted=False).order_by("-Id")
        return list
    except Exception as ex:
        return None

def get_All_Banks_Accounts_by_UserId(userId):
    try:
        account=BankAccounts.objects.select_related("userId").filter(isDeleted=False,userId=userId).order_by("-Id")
        return account
    except:
        return None

def get_Account_By_Name(bank_name):
    try:
        category=BankAccounts.objects.select_related("userId").get(isDeleted=False,bank_name=bank_name)
        return category
    except:
        return None