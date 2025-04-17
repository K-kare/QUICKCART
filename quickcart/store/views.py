from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm
from payment.form import ShippingForm
from payment.models import ShippingAddress
from django import forms


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searched = Product.objects.filter(name__icontains=searched)

        if  not searched:
             messages.success(request, "That Product Does Not Exist....Please try again")
             return render(request, 'search.html', {})
        else:
             return render(request, 'search.html', {'searched':searched})	
    else:
        return render(request, 'search.html', {})	
     

def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated...")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
          
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user )
        if user_form.is_valid() or shipping_form.is_valid():

            user_form.save()
            shipping_form.save()
            login(request, current_user)
            messages.success(request, "User Has Been Updated!!")
            return redirect('home')
        return render(request, "update_user.html", {'user_form':user_form , "shipping_form":shipping_form })
    else:
        messages.success(request, "You Must Be Logged In To Access That Page!!")
        return redirect('home')

    
 
def category_summary(request):
	categories = Category.objects.all()
	return render(request, 'category_summary.html', {"categories":categories})	

def category(request, kare):
    kare = kare.replace('-', '')
    try:
        category = Category.objects.get(name=kare)
        product = Product.objects.filter(category=category)
        return render(request, 'category.html', {'product':product, 'category':category} )
    except:
        messages.success(request, 'That Category does not exist')
        return redirect('home')


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product' : product})


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    products = Product.objects.all()
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have beeen logged In')
            return redirect('home')
        else:
            messages.success(request, 'There was an error Please try again')
            return redirect('login')

    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been Logged Out')
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')  
            password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have Registered Successfully!!') 
            return redirect('home')
        else:
            messages.error(request, 'There was a problem registering. Please check your details.')  
            return redirect('register')

    return render(request, 'register.html', {'form': form})  
