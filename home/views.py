from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.models import User
from home.models import *
# Create your views here.
class Base(View):
    views = {}
    views['categories'] = Category.objects.all()
    views['brands'] = Brand.objects.all()
def count_cart(request):
    username = request.user.username
    cart_number = Cart.objects.filter(username = username, checkout = False).count()
    return cart_number
class HomeView(Base):
    def get(self,request):
        self.views #initialization of above queries  categories,brand
        self.views['sliders'] = Slider.objects.all()
        self.views['ads'] = Ad.objects.all()
        self.views['brands'] = Brand.objects.all()
        self.views['hots'] = Product.objects.filter(labels = 'hot')
        self.views['news'] = Product.objects.filter(labels = 'new')
        self.views['sale'] = Product.objects.filter(labels = 'sale')
        return render(request,'index.html',self.views)

class CategoryView(Base):
    def get(self,request,slug):
        self.views
        ids = Category.objects.get(slug = slug).id #id= primary key
        self.views['product_category'] = Product.objects.filter(category_id = ids)
        return render(request,'category.html',self.views)

class BrandView(Base):
    def get(self,request,slug):
        self.views
        ids = Brand.objects.get(slug = slug).id #id= primary key
        self.views['product_brand'] = Product.objects.filter(brand_id = ids)
        return render(request,'brand.html',self.views)
class ProductDetailView(Base):
    def get(self,request,slug):
        self.views
        self.views['product_detail'] = Product.objects.filter(slug = slug)
        self.views['product_review'] = ProductReview.objects.filter(slug = slug)

        return render(request,'product-detail.html',self.views)

class SearchView(Base):
    def get(self, request):
        self.views
        self.views['cart_no'] = count_cart(request)
        query = request.GET.get('query')
        if query !='':  
            self.views['search_product'] = Product.objects.filter(name__icontains = query)
        else: 
            return redirect('/')
        return render(request, 'search.html', self.views)

def productReview(request,slug):
    if request.method == "POST":
       username = request.user.username
       email = request.user.email
       review = request.POST['review']
       star = request.POST['star']
       data = ProductReview.objects.create(
           name = username,
           email = email,
           review = review,
           star = star,
           slug = slug,
       )
       data.save()
    return redirect(f'/product/{slug}')

def SignUp(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username = username).exists():
                messages.error(request,"The Username is already taken!")
                return redirect('/signup')
            elif User.objects.filter(email = email).exists():
                messages.error(request,"Email is already in use!")
                return redirect('/signup')
            else:
                user = User.objects.create(
                    username = username,
                    email = email,
                    first_name = first_name,
                    last_name = last_name,
                    password = password,
                )
                user.save()
                messages.success(request,"Your Account is Succesfully Created!")    
                return redirect('/signup')
        else:
            messages.error(request,"The password and confirm password is not same!")
            return redirect('/signup')
            
    return render(request,'signup.html')

class CartView(Base):
    def get(self,request):
        self.views
        self.views['cart_no'] = count_cart(request)
        username = request.user.username
        cart_info = Cart.objects.filter(username = username, checkout = False)
        self.views['cart_product'] = cart_info
        all_total = 0
        for i in cart_info:
            all_total = all_total + i.total
        self.views['all_total'] = all_total
        self.views['shipping'] = 50
        self.views['grand_total'] = all_total + self.views['shipping']
        return render(request, 'cart.html', self.views)

def add_to_cart(request,slug):
    username = request.user.username
    if Cart.objects.filter(slug = slug, username=username, checkout = False).exists():
        quantity = Cart.objects.get(slug = slug, username= username,checkout=False).quantity
        price = Product.objects.get(slug = slug).price
        discounted_price = Product.objects.get(slug = slug).discounted_price
        if discounted_price > 0:
            original_price = discounted_price
        else:
            original_price = price

        quantity = quantity + 1
        total = quantity * original_price
        Cart.objects.filter(slug = slug, username=username, checkout = False).update(total = total,quantity = quantity)  
        return redirect('/cart')
    else:
        price = Product.objects.get(slug = slug).price
        discounted_price = Product.objects.get(slug = slug).discounted_price
        if discounted_price > 0:
            total = discounted_price
        else:
            total = price
        data = Cart.objects.create(
            username = username,
            slug = slug,
            items = Product.objects.filter(slug = slug)[0],
            total = total
        )
        data.save()
        return redirect('/cart')
    
def delete_cart(request,slug):
    username = request.user.username
    Cart.objects.filter(slug = slug, username= username,checkout=False).delete()
    return redirect('/cart')
            
def reduce_cart(request,slug):
    username = request.user.username
    if Cart.objects.filter(slug = slug, username=username, checkout = False).exists():
        quantity = Cart.objects.get(slug = slug, username= username,checkout=False).quantity
        price = Product.objects.get(slug = slug).price
        discounted_price = Product.objects.get(slug = slug).discounted_price
        if discounted_price > 0:
            original_price = discounted_price
        else:
            original_price = price
        if quantity > 1:
            quantity = quantity - 1
            total = quantity * original_price
            Cart.objects.filter(slug = slug, username=username, checkout = False).update(total = total,quantity = quantity)  
            return redirect('/cart')
        else:
            messages.error(request,'The quantity is already 1! if you want to reduce it delete it!')
            return redirect('/cart')