import base64
import json
import math
import os
from datetime import datetime
from django.core.mail import EmailMessage
from Baedin import settings
from Baedin.settings import BASE_DIR


def send_Mail(subject, text, UserName, Email):
    try:
        message = open("Baedin/templates/EmailTemplate.html")
        message = message.readlines()
        message = "".join(message)
        message = message.replace("{{username}}", UserName).replace("{{data}}", text)
        # print(message, "mail")
        mail = EmailMessage(
            subject,
            message,
            "Baedin. <" + settings.EMAIL_HOST_USER + ">",
            [Email]
        )
        mail.content_subtype = "html"
        # msg = (mail.subject, mail.body, mail.from_email, mail.to)
        mail.send()
        print("sent")
    except Exception as ex:
        print(ex)

def send_Mail_with_attachment(subject, text, userName, email,attachFileNames):
    try:
        # attachFileNames = json.loads(attachFileNames)
        message = open("Baedin/templates/EmailTemplate.html")
        message = message.readlines()
        message = "".join(message)
        message = message.replace("{{username}}", userName).replace("{{data}}", text)
        # print(message, "mail")
        mail = EmailMessage(
            subject,
            message,
            "baedin <" + settings.EMAIL_HOST_USER + ">",
            [email]
        )
        if (len(attachFileNames) > 0):
            fileName = []
            files = attachFileNames
            for f in files:
                url = f["filePath"]
                url = url.split(",")
                filedata = base64.b64decode(url[1])
                name = str(math.trunc(datetime.now().timestamp())) + "_" + f[
                    'fileName']
                filename = BASE_DIR + r"\Baedin\Attachments\\" + name  # I assume you have a way of picking unique filenames
                with open(filename, 'wb') as f:
                    f.write(filedata)
                    f.close()
                mail.attach_file(filename)
                fileName.append(filename)
            for f in fileName:
                if (os.path.exists(f)):
                    os.remove(f)
        mail.content_subtype = "html"
        # msg = (mail.subject, mail.body, mail.from_email, mail.to)
        mail.send()
        print("sent")
    except Exception as ex:
        print(ex)

import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp)
        )
account_activation_token = AccountActivationTokenGenerator()