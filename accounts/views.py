from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User



def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request,'Username already exists')
            return redirect('register')
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            return redirect('login')
    return render(request,'register.html')
    


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('student_list')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('login')
    return render(request,'login.html')



def user_logout(request):
    logout(request)
    return redirect('login')
