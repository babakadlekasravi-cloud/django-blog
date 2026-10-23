from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms  import UserCreationForm
from accounts.models import PasswordReset
from django.urls import reverse
from django.core.mail import EmailMessage
from django.utils import timezone
from accounts.forms import EmailUserCreationForm





# Create your views here.
def login_view(request):
    
    if request.method=="POST":
        username_or_email=request.POST.get('username')
        password=request.POST.get('password')

        if len(password)<3:
            messages.error(request,'password must be at least 3 chaaracters')


        if "@" in username_or_email:
            try:
                user=User.objects.get(email=username_or_email)
                username=user.username
            except User.DoesNotExist:
                username=None
        else:
            username=username_or_email

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.error(request,'Invalid login')
            return redirect('accounts:login')



    return render   (request,'accounts/login.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method=="POST":
       form=EmailUserCreationForm(request.POST)
       if form.is_valid():
           form.save()
           return redirect('/')
    else:
        form=EmailUserCreationForm()


    return render(request, 'accounts/signup.html',{'form': form})

def ForgotPassword(request):
    if request.method=="POST":
        email=request.POST.get('email')

        try: 
            user=User.objects.get(email=email)

            new_password_reset=PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url=reverse('accounts:reset-password',kwargs={'reset_id':new_password_reset.reset_id})
            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'
            email_body=f'Reset Your password using the link below:\n\n\n{full_password_reset_url}'


            email_message=EmailMessage(
                'Reset your password',
                email_body,
                "noerply@example.com",
                [email]

            )
    
            email_message.send(fail_silently=False)

            return redirect('accounts:password-reset-sent', reset_id=new_password_reset.reset_id)


        except User.DoesNotExist:
            messages.error(request,f"No user with '{email}' found")
            return redirect('accounts:forgot-password')


    return render(request,"accounts/forgot_password.html")

def PasswordResetSent(request,reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request,"accounts/password_reset_sent.html")
    else:
        messages.error(request,'Invalid reset id')
        return redirect('accounts:forgot-password')
 

def ResetPassword(request,reset_id):
    try:
        password_reset_id=PasswordReset.objects.get(reset_id=reset_id)
        if request.method=="POST":
            password=request.POST.get('password1')
            confirm_password=request.POST.get('password2')

            passwords_have_error=False
            if password != confirm_password:
                passwords_have_error=True
                messages.error(request,"Passwords do not match")
            if len(password)<3:
                passwords_have_error=True
                messages.error(request,'Password must be at least 3 characters')

            expiration_time=password_reset_id.created_when+timezone.timedelta(minutes=10)

            if timezone.now()>expiration_time:
                passwords_have_error=True
                messages.error(request,"reset link has expired")
                password_reset_id.delete()
                return redirect("accounts:forgot-password")
               

            if not passwords_have_error:
                user=password_reset_id.user
                user.set_password(password)
                user.save()

                password_reset_id.delete()


                messages.success(request,"Password reset proceed to login")

                return redirect('accounts:login')
            else:
                return redirect('accounts:reset-password',reset_id=reset_id)
            
    except PasswordReset.DoesNotExist:
        messages.error(request,"Invaid reset id")
        return redirect('accounts:forgot-password')
    return render(request,"accounts/reset_password.html",{'reset_id':reset_id})