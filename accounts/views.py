from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact

def register(request):
    if request.method == 'POST':
        # get form data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email is being used")
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                    user.save()
                    messages.success(request, 'registered successfully !!!')
                    return redirect('login')
        else:
            messages.error(request, "Password don't match") 
            return redirect('register')
         
        return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        # get form data
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Your log in Successfuly !!!')
            return redirect('dashboard')
        else:
            messages.error(request, 'invalid credentials')
            return redirect('dashboard')
    else:
        return render(request, 'accounts/login.html')
    

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Logged out Successfully.')
        return redirect('index')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts': user_contacts,
    }

    return render(request, 'accounts/dashboard.html', context)