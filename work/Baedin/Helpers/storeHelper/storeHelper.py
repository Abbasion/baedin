from Baedin_app.Models.Categories.categories import Categories
from Baedin_app.Models.Stores.store import Store


def get_Store_By_Id(Id):
    try:
        store=Store.objects.select_related("userId","category").get(isDeleted=False,pk=Id)
        return store
    except:
        return None

def get_All_Stores():
    try:
        list = Store.objects.select_related("userId","category").filter(isDeleted=False).order_by("-Id")
        return list
    except Exception as ex:
        return None

def get_Store_By_Name(store_name):
    try:
        store=Store.objects.select_related("userId","category").filter(isDeleted=False,store_name=store_name).order_by("-Id")
        return store
    except:
        return None

def get_Store_by_UserId(userId):
    try:
        store=Store.objects.select_related("userId","category").filter(isDeleted=False,userId=userId).order_by("-Id")
        return store
    except:
        return None

def get_Store_by_Category_name(category_name):
    try:
        store=Store.objects.select_related("userId","category").filter(isDeleted=False,category__category_name=category_name).order_by("-Id")
        return store
    except:
        return None

def get_Store_by_Category_Id(Id):
    try:
        store=Store.objects.select_related("userId","category").filter(isDeleted=False,category__Id=Id).order_by("-Id")
        return store
    except:
        return None

def get_Category_By_Name(category_name):
    try:
        category=Categories.objects.select_related("userId").get(isDeleted=False,category_name=category_name)
        return category
    except:
        return None