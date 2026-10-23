from django.contrib import admin
from django.urls import path
from accounts.views import *

app_name='accounts'
urlpatterns=[
    path('login',login_view,name="login"),
    path('logout',logout_view,name="logout"),
    path('signup',signup_view,name="signup"),
    path('forgot_password/',ForgotPassword,name="forgot-password"),
    path('password_reset_sent/<str:reset_id>/',PasswordResetSent,name="password-reset-sent"),
    path('reset_password/<str:reset_id>/',ResetPassword,name="reset-password")

]
