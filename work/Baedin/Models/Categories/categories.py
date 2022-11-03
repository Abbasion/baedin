import base64
import math
import os
from datetime import datetime

from django.forms import model_to_dict
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Baedin import settings
from Baedin.Helpers.Users.Users import getUser_by_Id
from Baedin.Helpers.categoriesHelper.categoriesHelper import get_Category_By_Id, get_All_Categories, \
    get_Categories_By_Name, get_Categories_by_UserId
from Baedin.Helpers.imgurlhelper.urlhelper import img_url, img_url_profile
from Baedin.settings import IMG_URL
from Baedin_app.Models.Categories.categories import Categories
from Baedin_app.Models.Users.userSerializer import UserSerializer


class CategoriesCreateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            d = request.data
            # d = json.loads(data)
            if ('Id' not in d.keys()):
                return Response(
                    {"data": "Id is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            if ('category_name' in d.keys()):
                category_name = d['category_name']
            else:
                return Response(
                    {"data": "category_name is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            user = request.user

            if (user is None):
                return Response({"data": "user doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            isDeleted = False
            if ('isDeleted' in d.keys()):
                isDeleted = d['isDeleted']
            categories = get_Categories_By_Name(d['category_name'])
            print(categories)


            if (d['Id'] == 0 or d['Id'] == None):

                if categories and isDeleted == False:
                    return Response(
                        {"data": "Category with this Name already exists",
                         "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )


                category = Categories(
                    userId=user,
                    category_name=category_name,
                    isDeleted=isDeleted

                )
                if ("category_icon" in d.keys()):
                    if not d['category_icon']:
                        return Response(
                            {"data": "Please upload you Category Icon", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    if (isinstance(d['category_icon'], str)):
                        return Response(
                            {"data": "Please upload you Category Icon", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    elif (isinstance(d['category_icon'], dict)):
                        if ("fileName" in d["category_icon"].keys()):
                            url = d['category_icon']["filePath"]
                            url = url.split(",")
                            filedata = base64.b64decode(url[1])
                            name = str(math.trunc(datetime.now().timestamp())) + "_" + d['category_icon'][
                                'fileName']
                            filename = str(settings.BASE_DIR) + r"\Baedin/uploads\\" + name
                            with open(filename, 'wb') as f:
                                f.write(filedata)
                                f.close()

                                category.category_icon = name
                else:
                    return Response(
                        {"data": "Profile Picture is required"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                category.save()

                data = model_to_dict(category)
                data['userId'] = (UserSerializer(category.userId)).data
                if (category.userId.profilePic):
                    data['userId']['profilePic'] = str(IMG_URL) + "/Baedin/uploads/" + str(category.userId.profilePic)
                newData = model_to_dict(category)
                newData['userId'] = (UserSerializer(category.userId)).data
                if (category.userId.profilePic):
                    pp = str(IMG_URL) + "/Baedin/uploads/" + str(category.userId.profilePic)
                    newData['userId']['profilePic'] = pp
                if (category.category_icon,dict):
                    pp = str(IMG_URL) + "/Baedin/uploads/" + str(category.category_icon)
                    newData['category_icon'] = pp

                return Response({"data": newData, "status": status.HTTP_201_CREATED}, status=status.HTTP_200_OK)

            else:
                category = Categories.objects.get(pk=d['Id'])

                if (category is None):
                    return Response({"data": "Category doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                    status=status.HTTP_404_NOT_FOUND)

                category.isDeleted = isDeleted
                if 'category_name' in d.keys():
                    if d['category_name']== category.category_name:
                        category.category_name = category.category_name
                    elif categories and isDeleted == False:
                        return Response(
                            {"data": "Category with this Name already exists",
                             "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
                    else:
                        category.category_name= d['category_name']


                if ("category_icon" in d.keys()):
                    if not d['category_icon']:
                        return Response(
                            {"data": "Please upload you Category Icon", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    if (isinstance(d['category_icon'], str)):
                        return Response(
                            {"data": "Please upload you Category Icon", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    elif (isinstance(d['category_icon'], dict)):
                        # if (isinstance(d['category_icon'], dict)):
                            if ("fileName" in d["category_icon"].keys()):
                                url = d['category_icon']["filePath"]
                                url = url.split(",")
                                filedata = base64.b64decode(url[1])
                                name = str(math.trunc(datetime.now().timestamp())) + "_" + d['category_icon'][
                                    'fileName']
                                filename = str(settings.BASE_DIR) + r"\Baedin/uploads\\" + name
                                with open(filename, 'wb') as f:
                                    f.write(filedata)
                                    f.close()

                                    if (category.category_icon):
                                        if os.path.exists(str(settings.BASE_DIR) + r"\Baedin/uploads\\" + category.category_icon):
                                            os.remove(str(settings.BASE_DIR) + r"\Baedin/uploads\\" + category.category_icon)

                                    category.category_icon = name

                category.save()
            data = model_to_dict(category)
            data['userId'] = (UserSerializer(category.userId)).data
            if (category.userId.profilePic):
                data['userId']['profilePic'] = str(IMG_URL) + "/Baedin/uploads/" + str(category.userId.profilePic)
            if (category.category_icon):
                pp = str(IMG_URL) + "/Baedin/uploads/" + str(category.userId.profilePic)
                data['category_icon'] = pp

            return Response({"data": data, "status": status.HTTP_201_CREATED}, status=status.HTTP_200_OK)

        except Exception as ex:
            return Response({"data": str(ex), "Status": status.HTTP_403_FORBIDDEN})

    def put(self, request, pk, format=None):
        try:
            data = []
            category = get_Category_By_Id(pk)
            if (category is None):
                return Response({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                data = model_to_dict(category)
                if (data['category_icon']):
                    data['category_icon'] = img_url(data['category_icon'])
                data['userId'] = (UserSerializer(category.userId)).data
                if (category.userId.profilePic):
                    data['userId']['profilePic'] = img_url_profile(category.userId.profilePic)
                return Response({"data": data, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data": str(ex), "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        try:

            data = []

            categories = get_All_Categories()
            if (categories is None):
                return Response({"data": "Cards doesn't exists", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            for category in categories:
                cat_data = model_to_dict(category)

                if (category.category_icon):
                    cat_data['cardPic'] = img_url(category.category_icon)
                cat_data['userId'] = UserSerializer(category.userId).data
                if (category.userId.profilePic):
                    cat_data['userId']['profilePic'] = img_url_profile(category.userId.profilePic)
                data.append(cat_data)

            return Response({"data": data, "Status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "Status": status.HTTP_403_FORBIDDEN})


class CategoriesListAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            d = request.data
            data = []
            if ('category_name' in d.keys()):
                category_name = d['category_name']
            else:
                return Response(
                    {"data": "category_name is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            categories = get_Categories_By_Name(d['category_name'])
            if (categories is None):
                return Response({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                for category in categories:
                    cat_data = model_to_dict(category)

                    if (category.category_icon):
                        cat_data['category_icon'] = img_url(category.category_icon)

                    cat_data['userId'] = UserSerializer(category.userId).data
                    if (category.userId.profilePic):
                        cat_data['userId']['profilePic'] = img_url_profile(category.userId.profilePic)
                    data.append(cat_data)

                return Response({"data": data, "Status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "Status": status.HTTP_403_FORBIDDEN})

    def get(self, request, pk, format=None):
        try:

            data = []
            categories = get_Categories_by_UserId(pk)
            for category in categories:
                cat_Data = model_to_dict(category)
                if (category.category_icon):
                    cat_Data['category_icon'] = img_url(category.category_icon)
                cat_Data['userId'] = UserSerializer(category.userId).data
                if (category.userId.profilePic):
                    cat_Data['userId']['profilePic'] = img_url(category.userId.profilePic)

                data.append(cat_Data)

            return Response({"data": data, "Status": status.HTTP_200_OK})
        except Exception as ex:
            return Response({"data": str(ex), "Status": status.HTTP_403_FORBIDDEN},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)