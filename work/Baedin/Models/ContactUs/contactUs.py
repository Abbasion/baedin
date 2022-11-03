import json
import threading

from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Baedin import settings
from Baedin.Helpers.ContactUsHelper.contactUsHelper import contact_us_by_Id, get_all_contact
from Baedin.Helpers.EmailHelper import emailHelper
from Baedin_app.Models.ContactUs.contactUs import ContactUs


class ContactUsListUpdate(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request,*args, **kwargs):
        try:
            data = request.data
            dic = json.dumps(data)
            dic = json.loads(dic)
            # contact = contact_us_by_Id(dic['Id'])
            if 'name' not in dic.keys():
                return Response(
                    {"data": "Name is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            if 'email' not in dic.keys():
                return Response(
                    {"data": "email is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            if 'phoneNumber' not in dic.keys():
                return Response(
                    {"data": "phoneNumber is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            if 'message' not in dic.keys():
                return Response(
                    {"data": "Message is required"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            isDeleted = False
            if ('isDeleted' in dic.keys()):
                isDeleted = dic['isDeleted']


            # if contact is None:
            con = ContactUs(

                    name=dic['name'],
                    email=dic['email'],
                    phoneNumber=dic['phoneNumber'],
                    message=dic['message'],
                    isDeleted=isDeleted

                )
            con.save()
            body = "We appreciate you contacting us " + con.name + ".One of our members will be getting back to you shortly. <br/><br/>"

            t = threading.Thread(target=emailHelper.send_Mail,
                                     args=("Contact Beadin", body, con.name, con.email))
            t.setDaemon(True)
            t.start()
            body2 = "Baedin User : <b>" + con.name + "</b>.sent a message having phone number <b>" + con.phoneNumber + "</b> , Email <b>" + con.email + "</b> and message <b>" + con.message + "</b>. <br/><br/>"

            t2 = threading.Thread(target=emailHelper.send_Mail,
                                  args=("Contact Us", body2, settings.EMAIL_HOST_NAME, settings.EMAIL_HOST_USER))
            t2.setDaemon(True)
            t2.start()

            cont = model_to_dict(con)
            return JsonResponse({"data": cont, "status": status.HTTP_201_CREATED}, status=status.HTTP_200_OK)
        except Exception as ex:
            return JsonResponse({"data": str(ex), "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, *args, **kwargs):
        try:
            data = []
            contact = contact_us_by_Id(pk)
            if (contact is None):
                return JsonResponse({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                data = model_to_dict(contact)

                return JsonResponse({"data": data, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except Exception as ex:
            return JsonResponse({"data": str(ex), "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        try:
            data = []
            contacts = get_all_contact()
            if (contacts is None):
                return JsonResponse({"data": "No record found", "status": status.HTTP_404_NOT_FOUND},
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                for cons in contacts:
                    con_data = model_to_dict(cons)
                    data.append(con_data)


                return JsonResponse({"data": data, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except Exception as ex:
            return JsonResponse({"data": str(ex), "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)