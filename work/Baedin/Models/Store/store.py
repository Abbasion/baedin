import base64
import datetime
import json
import math
import os

from django.forms import model_to_dict
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Baedin import settings
from Baedin.Helpers.Users.Users import getUser_by_Id
from Baedin.Helpers.categoriesHelper.categoriesHelper import get_Category_By_Id
from Baedin.Helpers.imgurlhelper.urlhelper import img_url, img_url_profile
from Baedin.Helpers.storeHelper.storeHelper import get_Store_By_Id, get_All_Stores, get_Store_By_Name, \
    get_Store_by_UserId, get_Store_by_Category_Id, get_Store_by_Category_name, get_Category_By_Name
from Baedin.settings import IMG_URL
from Baedin_app.Models.Stores.store import Store
from Baedin_app.Models.Users.userSerializer import UserSerializer


class StoreCreateAPIView(RetrieveUpdateAPIView):
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
            if 'category' not in d.keys():
                return Response(
                    {"data": "category is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            category = get_Category_By_Id(d['category'])
            if (category is None):
                return Response({"data": "category doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            isDeleted = False
            if ('isDeleted' in d.keys()):
                isDeleted = d['isDeleted']

            if (d['Id'] == 0 or d['Id'] == None):
                if ('store_name' in d.keys()):
                    store_name = d['store_name']
                else:
                    return Response(
                        {"data": "Store Name is required"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                store = Store(
                    userId=user,
                    category=category,
                    store_name=store_name,
                    isDeleted=isDeleted

                )
                if ("store_logo" in d.keys()):
                    if not d['store_logo']:
                        return Response(
                            {"data": "Please upload you store_logo", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    if (isinstance(d['store_logo'], str)):
                        return Response(
                            {"data": "Please upload you Store Logo", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    elif (isinstance(d['store_logo'], dict)):
                        if ("fileName" in d["store_logo"].keys()):
                            url = d['store_logo']["filePath"]
                            url = url.split(",")
                            filedata = base64.b64decode(url[1])
                            name = str(math.trunc(datetime.datetime.now().timestamp())) + "_" + d['store_logo'][
                                'fileName']
                            filename = str(settings.BASE_DIR) + r"\Baedin/uploads\\" + name
                            with open(filename, 'wb') as f:
                                f.write(filedata)
                                f.close()

                                store.store_logo = name
                else:
                    return Response(
                        {"data": "Store Logo is required"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                store.save()

                data = model_to_dict(store)
                data['category'] = model_to_dict(store.category)
                data['category']['userId'] = model_to_dict(store.category.userId)
                data['userId'] = (UserSerializer(store.userId)).data
                newData = model_to_dict(store)
                newData['category'] = model_to_dict(store.category)
                # newData['category']['userId'] = model_to_dict(store.category.userId)
                newData['userId'] = (UserSerializer(store.userId)).data
                if (store.userId.profilePic):
                    pp = str(IMG_URL) + "/Baedin/uploads/" + str(store.userId.profilePic)
                    newData['userId']['profilePic'] = pp
                if (store.category.category_icon):
                    pp = str(IMG_URL) + "/Baedin/uploads/" + str(store.category.category_icon)
                    newData['category']['category_icon'] = pp
                # if (store.category.userId.profilePic):
                #     pp = str(IMG_URL) + "/Baedin/uploads/" + str(store.category.userId.profilePic)
                #     newData['category']['userId']['profilePic'] = pp
                if (store.store_logo):
                    pp = str(IMG_URL) + "/Baedin/uploads/" + str(store.store_logo)
                    newData['store_logo'] = pp


                return Response({"data": newData, "status": status.HTTP_201_CREATED}, status=status.HTTP_200_OK)

            else:
                store = Store.objects.get(pk=d['Id'])
                if (store is None):
                    return Response({"data": "Store doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                    status=status.HTTP_404_NOT_FOUND)
                if d['category'] == store.category.Id:


                    # store.userId = user,
                    # store.category = category,
                    store.isDeleted = isDeleted
                    if 'store_name' in d.keys():
                        store.store_name = d['store_name']

                    if ("store_logo" in d.keys()):
                        if not d['store_logo']:
                            return Response(
                                {"data": "Please upload you store_logo", "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                        if (isinstance(d['store_logo'], str)):
                            return Response(
                                {"data": "Please upload you Store Logo", "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                        elif (isinstance(d['store_logo'], dict)):
                            if (isinstance(d['store_logo'], dict)):
                                if ("fileName" in d["store_logo"].keys()):
                                    url = d['store_logo']["filePath"]
                                    url = url.split(",")
                                    filedata = base64.b64decode(url[1])
                                    name = str(math.trunc(datetime.datetime.now().timestamp())) + "_" + d['store_logo'][
                                        'fileName']
                                    filename = str(settings.BASE_DIR) + r"\Baedin/uploads\\" + name
                                    with open(filename, 'wb') as f:
                                        f.write(filedata)
                                        f.close()

                                        if (store.store_logo):
                                            if os.path.exists(str(settings.BASE_DIR) + r"\Baedin/uploads\\" + store.store_logo):
                                                os.remove(str(settings.BASE_DIR) + r"\Baedin/uploads\\" + store.store_logo)

                                        store.store_logo = name

                    store.save()
                    data = model_to_dict(store)
                    data['category'] = model_to_dict(store.category)
                    # data['category']['userId'] = model_to_dict(store.category.userId)
                    data['userId'] = (UserSerializer(store.userId)).data
                    newData = model_to_dict(store)
                    newData['category'] = model_to_dict(store.category)
                    # newData['category']['userId'] = model_to_dict(store.category.userId)
                    newData['userId'] = (UserSerializer(store.userId)).data
                    if (store.userId.profilePic):
                        pp = str(IMG_URL) + "/Baedin/uploads/" + str(store.userId.profilePic)
                        newData['userId']['profilePic'] = pp
                    if (store.category.category_icon):
                        pp = str(IMG_URL) + "/Baedin/uploads/" + str(store.category.category_icon)
                        newData['category']['category_icon'] = pp
                    # if (store.category.userId.profilePic):
                    #     pp = str(IMG_URL) + "/Baedin/uploads/" + str(store.category.userId.profilePic)
                    #     newData['category']['userId']['profilePic'] = pp
                    if (store.store_logo):
                        pp = str(IMG_URL) + "/Baedin/uploads/" + str(store.store_logo)
                        newData['store_logo'] = pp
                else:
                    return Response({"data": "Store category doesn't match", "status": status.HTTP_404_NOT_FOUND},
                                    status=status.HTTP_404_NOT_FOUND)

            return Response({"data": newData, "status": status.HTTP_201_CREATED}, status=status.HTTP_200_OK)

        except Exception as ex:
            return Response({"data": str(ex), "Status": status.HTTP_403_FORBIDDEN})

    def put(self, request, pk, format=None):
        try:
            data = []
            store = get_Store_By_Id(pk)
            if (store is None):
                return Response({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                data = model_to_dict(store)
                if (store.store_logo):
                    data['store_logo'] = img_url(store.store_logo)
                if (store.category):
                    data['category_name'] = store.category.category_name
                # data["category"]= model_to_dict(store.category)
                # if (store.category.category_icon):
                #     data['category']['category_icon'] = img_url_profile(store.category.category_icon)
                # data["category"]["userId"] = model_to_dict(store.category.userId)
                # if (store.category.userId.profilePic):
                #     data['category']['userId']["profilePic"] = img_url_profile(store.category.userId.profilePic)
                # data['userId'] = (UserSerializer(store.userId)).data
                # if (store.userId.profilePic):
                #     data['userId']['profilePic'] = img_url_profile(store.userId.profilePic)
                return Response({"data": data, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def get(self, request, *args, **kwargs):
        try:

            data = []

            stores = get_All_Stores()
            if (stores is None):
                return Response({"data": "Cards doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            for store in stores:
                store_data = model_to_dict(store)
                if (store.store_logo):
                    store_data['store_logo'] = img_url(store.store_logo)
                if( store.category):
                    store_data['category_name'] = store.category.category_name
                # store_data["category"] = model_to_dict(store.category)
                # if (store.category.category_icon):
                #     store_data['category']['category_icon'] = img_url_profile(store.category.category_icon)
                # store_data["category"]["userId"] = model_to_dict(store.category.userId)
                # if (store.category.userId.profilePic):
                #     store_data["category"]["userId"]["profilePic"] = img_url_profile(store.category.userId.profilePic)
                # store_data['userId'] = (UserSerializer(store.userId)).data
                # if (store.userId.profilePic):
                #     store_data['userId']['profilePic'] = img_url_profile(store.userId.profilePic)
                data.append(store_data)

            return Response({"data": data, "Status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "Status": status.HTTP_403_FORBIDDEN})


class StoreListAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            d = request.data
            data = []
            if not d['store_name']:
                return Response(
                    {"data": "Store Name is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            stores = get_Store_By_Name(d['store_name'])
            if (stores is None):
                return Response({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                for store in stores:
                    store_data = model_to_dict(store)
                    if (store.store_logo):
                        store_data['store_logo'] = img_url(store.store_logo)
                    if (store.category):
                        store_data['category_name'] = store.category.category_name
                    # store_data["category"] = model_to_dict(store.category)
                    # if (store.category.category_icon):
                    #     store_data['category']['category_icon'] = img_url_profile(store.category.category_icon)
                    # store_data["category"]["userId"] = model_to_dict(store.category.userId)
                    # if (store.category.userId.profilePic):
                    #     store_data["category"]["userId"]["profilePic"] = img_url_profile(
                    #         store.category.userId.profilePic)
                    # store_data['userId'] = (UserSerializer(store.userId)).data
                    # if (store.userId.profilePic):
                    #     store_data['userId']['profilePic'] = img_url_profile(store.userId.profilePic)
                    data.append(store_data)

                return Response({"data": data, "Status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "Status": status.HTTP_403_FORBIDDEN})

    def get(self, request, pk, format=None):
        try:

            data = []
            stores = get_Store_by_UserId(pk)
            if (stores is None):
                return Response({"data": "Store No record found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            # category = get_Category_By_Name('category_name')
            # if (category is None):
            #     return Response({"data": "Category No record found", "status": status.HTTP_404_NOT_FOUND},
            #                     status=status.HTTP_404_NOT_FOUND)
            # cat = model_to_dict(category)
            list = {}
            list.update({"category": ""})
            for store in stores:
                store_data = model_to_dict(store)
                if (store.store_logo):
                    store_data['store_logo'] = img_url(store.store_logo)
                # store_data["category"] = model_to_dict(store.category)
                # if (store.category.category_icon):
                #     store_data['category']['category_icon'] = img_url_profile(store.category.category_icon)
                # store_data["category"]["userId"] = model_to_dict(store.category.userId)
                # if (store.category.userId.profilePic):
                #     store_data["category"]["userId"]["profilePic"] = img_url_profile(
                #         store.category.userId.profilePic)
                # store_data['userId'] = (UserSerializer(store.userId)).data
                # if (store.userId.profilePic):
                #     store_data['userId']['profilePic'] = img_url_profile(store.userId.profilePic)
                data.append(store_data)

                # list["category"].update({"stores": data})

            return Response({"data": data, "Status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "Status": status.HTTP_403_FORBIDDEN},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class StoreBYCategory(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            d = request.data
            data = []
            if not d['category_name']:
                return Response(
                    {"data": " category_name is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            stores = get_Store_by_Category_name(d['category_name'])
            if (stores is None):
                return Response({"data": "No Store record found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            category = get_Category_By_Name(d['category_name'])
            if (category is None):
                return Response({"data": "No Category record found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            cat = model_to_dict(category)
            list = {}
            list.update({"category": cat})

            for store in stores:
                new_list = model_to_dict(store)
                if (store.store_logo):
                    new_list['store_logo'] = img_url(store.store_logo)
                # store_data["category"] = model_to_dict(store.category)
                # if (store.category.category_icon):
                #     store_data['category']['category_icon'] = img_url_profile(store.category.category_icon)
                # store_data["category"]["userId"] = model_to_dict(store.category.userId)
                # if (store.category.userId.profilePic):
                #     store_data["category"]["userId"]["profilePic"] = img_url_profile(
                #         store.category.userId.profilePic)
                # store_data['userId'] = (UserSerializer(store.userId)).data
                # if (store.userId.profilePic):
                #     store_data['userId']['profilePic'] = img_url_profile(store.userId.profilePic)
                data.append(new_list)
                list["category"].update({"stores": data})

            return Response({"data": list, "Status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "Status": status.HTTP_403_FORBIDDEN})

    def get(self, request, pk, format=None):
        try:

            data = []
            stores = get_Store_by_Category_Id(pk)
            if (stores is None):
                return Response({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            category = get_Category_By_Id(pk)
            if (category is None):
                return Response({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            cat = model_to_dict(category)
            list ={}
            list.update({"category":cat})

            for store in stores:
                newlist = model_to_dict(store)
                if (store.store_logo):
                    newlist['store_logo'] = img_url(store.store_logo)
                # category["category"] = model_to_dict(store.category)
                # if (store.category.category_icon):
                #     category['category']['category_icon'] = img_url_profile(store.category.category_icon)
                # category["category"]["userId"] = model_to_dict(store.category.userId)
                # if (store.category.userId.profilePic):
                #     category["category"]["userId"]["profilePic"] = img_url_profile(
                #         store.category.userId.profilePic)
                # category['userId'] = (UserSerializer(store.userId)).data
                # if (store.userId.profilePic):
                #     category['userId']['profilePic'] = img_url_profile(store.userId.profilePic)
                # data.append(newlist)
                #
                data.append(newlist)
                list["category"].update({"stores":data})

            return Response({"data": list, "Status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "Status": status.HTTP_403_FORBIDDEN},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

