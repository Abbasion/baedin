from django.contrib import admin
from django.urls import path

from Baedin.Models.AddData.AddData import addData
from Baedin.Models.AdminWallet.adminWallet import AdminWalletListUpdateAPIView
from Baedin.Models.BankAccounts.bankAccounts import BankAccountCreate
from Baedin.Models.Categories.categories import CategoriesCreateAPIView, CategoriesListAPIView
from Baedin.Models.ContactUs.contactUs import ContactUsListUpdate
from Baedin.Models.ForgetPassword.forgetPassword import Forget_password, resendActivationLink, Reset
from Baedin.Models.Store.store import StoreCreateAPIView, StoreListAPIView, StoreBYCategory
from Baedin.Models.Wallet.wallet import WalletsByUserIdUpdateAPIView, WalletListUpdateAPIView
from Baedin.Models.login.login import CreateUserAPIView, Login, UserRetrieveUpdateAPIView, TokenVerify, \
    AdminRetrieveUpdateAPIView

urlpatterns = [
    path('migrate/', addData),
    path('user/registration/', CreateUserAPIView.as_view()),
    path('user/update/', CreateUserAPIView.as_view()),
    path('login/', Login),
    path('verify/token/', TokenVerify.as_view(), name='token_verify'),
    path('user/all/', UserRetrieveUpdateAPIView.as_view()),
    path('user/<int:pk>/', UserRetrieveUpdateAPIView.as_view()),
    path('user/phone/', UserRetrieveUpdateAPIView.as_view()),
    path('user/email/', UserRetrieveUpdateAPIView.as_view()),
    path('user/all/admin/', AdminRetrieveUpdateAPIView.as_view()),
    path('admin/wallet/increment/', AdminWalletListUpdateAPIView.as_view()),
    path('admin/wallet/decrement/', AdminWalletListUpdateAPIView.as_view()),
    path('admin/wallet/<int:pk>/', AdminWalletListUpdateAPIView.as_view()),
    path('user/wallet/<int:pk>/', WalletsByUserIdUpdateAPIView.as_view()),
    path('user/wallet/update/', WalletsByUserIdUpdateAPIView.as_view()),
    path('wallet/<str:pk>/', WalletListUpdateAPIView.as_view()),
    path('wallet/', WalletListUpdateAPIView.as_view()),
    # path('wallet/update/', WalletListUpdateAPIView.as_view()),
    path('category/create/', CategoriesCreateAPIView.as_view()),
    path('category/update/', CategoriesCreateAPIView.as_view()),
    path('categories/all/', CategoriesCreateAPIView.as_view()),
    path('category/<int:pk>/', CategoriesCreateAPIView.as_view()),
    path('category/name/', CategoriesListAPIView.as_view()),
    path('category/by/user/<int:pk>/', CategoriesListAPIView.as_view()),
    path('store/create/', StoreCreateAPIView.as_view()),
    path('store/update/', StoreCreateAPIView.as_view()),
    path('store/all/', StoreCreateAPIView.as_view()),
    path('store/<int:pk>/', StoreCreateAPIView.as_view()),
    path('store/name/', StoreListAPIView.as_view()),
    path('store/by/user/<int:pk>/', StoreListAPIView.as_view()),
    path('store/by/category/name/', StoreBYCategory.as_view()),
    path('store/by/category/id/<int:pk>/', StoreBYCategory.as_view()),
    path('bank/account/create/', BankAccountCreate.as_view()),
    path('bank/account/update/', BankAccountCreate.as_view()),
    path('bank/account/all/', BankAccountCreate.as_view()),
    path('bank/account/by/id/<int:pk>/', BankAccountCreate.as_view()),
    path('bank/account/by/userid/<int:pk>/', BankAccountCreate.as_view()),
    path('contact/us/', ContactUsListUpdate.as_view()),
    path('contact/us/<int:pk>/', ContactUsListUpdate.as_view()),
    path('forget/password/', Forget_password.as_view()),
    path('resend/email/<str:uid>/', resendActivationLink),
    path('reset/<uidb64>/<token>/', Reset, name="reset_pass"),
]
