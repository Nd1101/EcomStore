from django.shortcuts import render,redirect
from .forms import CustomUserForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
# Create your views here.
def Home(request):
    products = Product.objects.filter(trending=1)
    return render(request,"Index.html",{"products": products})

def Login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username=name, password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully")
                return redirect("/")
            else:
                messages.error(request, "Invalid User Name or Password")
                return redirect("/login")
        return render(request, "LogIn.html")

def Logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully!")
    return redirect("/")

def Cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, "Cart.html", {"cart": cart})
    else:
        return redirect("/")

def Remove_cart(request,cid):
    cartitem = Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")


def Register(request):
    form=CustomUserForm()
    if request.method =='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Successfully Registered You can Login Now...")
            return redirect('/login')
    return render(request,"register.html",{'form':form})

def Collection(request):
    category=Category.objects.filter(status=0)
    return render(request,"Collections.html",{"category":category})

def CollectionView(request,name):
    if(Category.objects.filter(name=name,status=0)):
        products=Product.objects.filter(category__name=name)
        return render(request, "ProductIndex.html", {"products": products,"category_name":name})
    else:
        messages.warning(request,"No such category found...")
        return redirect('/collections')

def ProductDetails(request,cname,pname):
    if (Category.objects.filter(name=cname, status=0)):
        if (Product.objects.filter(name=pname, status=0)):
            products = Product.objects.filter(name=pname, status=0).first()
            return render(request, "Productdetails.html", {"products": products})
        else:
            messages.error(request, "No such product found...")
            return redirect('/collections')
    else:
        messages.warning(request, "No such category found...")
        return redirect('/collections')

def Add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty = data['product_qty']
            product_id = data['pid']
            # print(request.user.id)
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id, product_id=product_id):
                    return JsonResponse({'status': 'Product Already in Cart'}, status=200)
                else:
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                        return JsonResponse({'status': 'Product Added to Cart'}, status=200)
                    else:
                        return JsonResponse({'status': 'Product Stock Not Available'}, status=200)
        else:
            return JsonResponse({'status': 'Login to Add Cart'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)

def Wishlist_page(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_id = data['pid']
            # print(request.user.id)
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if Wishlist.objects.filter(user=request.user.id, product_id=product_id):
                    return JsonResponse({'status': 'Product Already in Wishlist'}, status=200)
                else:
                    Wishlist.objects.create(user=request.user, product_id=product_id)
                    return JsonResponse({'status': 'Product Added to Wishlist'}, status=200)

        else:
            return JsonResponse({'status': 'Login to Add Wishlist'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)

def Wishlist_Viewpage(request):
    if request.user.is_authenticated:
        fav= Wishlist.objects.filter(user=request.user)
        return render(request, "Favorite.html", {"fav": fav})
    else:
        return redirect("/")

def Remove_fav(request,fid):
    item = Wishlist.objects.get(id=fid)
    item.delete()
    return redirect("/favviewpage")

def Blog_page(request):
    return render(request,"Blog.html")

def About_page(request):
    return render(request,"About.html")

def Faq_page(request):
    return render(request,"Faq.html")