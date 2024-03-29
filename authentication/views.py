from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail

from loginsignup import settings
def home(request):
    return render(request,"authentication/index.html")

def signup(request):
    if request.method=="POST":
        # username = request.POST.get('username')  we can also get value from user like this....
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['mail']
        password = request.POST['password']
        confirmPassword = request.POST['conpassword']


        if User.objects.filter(username=username):
            messages.error(request,'username already exixts')
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request,'email id already exists')
            return redirect('home')
        
        if len(username)>10:
            messages.error(request,"username must be within ten char")

        if password != confirmPassword:
            messages.error(request,'passwords are missmatching ')
        
        if not username.isalnum():
            messages.error(request,'username only contain char and num')
            return redirect('home')
        


        myuser = User.objects.create_user(username,email,password)
        myuser.first_name = firstname
        myuser.last_name = lastname

        myuser.save()
        messages.success(request,"Your account has been created successfully and we sent an confimation mail")
        return redirect('signin')
    
        #welcome mail for the user

        subject = "Welcome to VCET-ECE"
        message = "Hello" + myuser.first_name + "!!!.. \n" "Welcome to the department of electronics and communication \n" + "Thankyou for visiting our page\n" + "Additionally we sent a confirmation mail for you please go to that mail and confirm your mail id in order to cereate your account"
        from_email = settings.EMAIL_HOST_USER
        to_email = [myuser.email]
        send_mail(subject,message,from_email,to_email, fail_silently=True)

        
    return render(request,'authentication/signup.html')
       
def signin(request):
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']

        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            firstname = user.first_name
            return render(request,'authentication/index.html',{'fname':firstname})
        else:
            messages.error(request,"Bad credentials")
            return redirect('signup')
        
    
    return render(request,'authentication/signin.html')
def signout(request):
    logout(request)
    messages.success(request,"logged out successfully")
    return redirect('home')