from Baedin_app.Models.Categories.categories import Categories


def get_All_Categories():
    try:
        list = Categories.objects.select_related("userId").filter(isDeleted=False).order_by("-Id")
        return list
    except Exception as ex:
        return None

def get_Category_By_Id(Id):
    try:
        category=Categories.objects.select_related("userId").get(isDeleted=False,pk=Id)
        return category
    except:
        return None

def get_Categories_By_Name(category_name):
    try:
        category=Categories.objects.select_related("userId").filter(isDeleted=False,category_name=category_name)
        return category
    except:
        return None


def get_Categories_by_UserId(userId):
    try:
        category=Categories.objects.select_related("userId").filter(isDeleted=False,userId=userId).order_by("-Id")
        return category
    except:
        return None