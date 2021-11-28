from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import Group
from .forms import *
from .models import *
import telepot
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

token = '1368490503:AAFPqjW7yUvDgtsokWF2qS8soiM0e393fA8'
bot = telepot.Bot(token)
my_id = 834592754

def home(request):
    category = Categories.objects.all()
    ls_products = Product.objects.all().order_by('-id')[:3]
    ls_posts = Post.objects.all().order_by('-id')[:3]
    context = {
        'ls_posts':ls_posts,
        'categories':category,
        'products':ls_products,
        'nbar':'home'
    }
    return render(request, 'home.html', context)

def product_detail(request, car_slug):
    product = get_object_or_404(Product, slug=car_slug)
    context =  {
                'product':product,
                'nbar':'car_detail',
                }
    return render(request, 'car-details.html',context)

def is_valid_queryparam(param):
    return param != '' and param is not None

def all_cars(request):
    qs = Product.objects.all()
    new = request.GET.get('new')
    used = request.GET.get('used')
    car_name = request.GET.get('car_name')
    model = request.GET.get('model')
    first_registration = request.GET.get('first_registration')
    price = request.GET.get('price')
    mileage = request.GET.get('mileage')
    engine_size = request.GET.get('engine_size')
    power = request.GET.get('power')
    fuel = request.GET.get('fuel')
    gearbox = request.GET.get('gearbox')
    if new == 'new':
        qs = qs.filter(new=True)
    if used == 'used':
        qs = qs.filter(new=False)
    if is_valid_queryparam(car_name) and car_name != 'sellect':
        qs = qs.filter(name__name=car_name)
    if is_valid_queryparam(model) and model != 'sellect':
        qs = qs.filter(model__model=model)
    if is_valid_queryparam(first_registration) and first_registration != 'sellect':
        qs = qs.filter(first_registration__first_registration=first_registration)
    if is_valid_queryparam(price) and price != 'sellect':
        qs = qs.filter(price__price=price)
    if is_valid_queryparam(mileage) and mileage != 'sellect':
        qs = qs.filter(mileage__mileage=mileage)
    if is_valid_queryparam(engine_size) and engine_size != 'sellect':
        qs = qs.filter(engine_size__engine_size=engine_size)
    if is_valid_queryparam(power) and power != 'sellect':
        qs = qs.filter(power__power=power)
    if is_valid_queryparam(fuel) and fuel != 'sellect':
        qs = qs.filter(fuel__fuel=fuel)
    if is_valid_queryparam(gearbox) and gearbox != 'sellect':
        qs = qs.filter(gearbox__gearbox=gearbox)
    all_car = Paginator(qs,9)
    page = request.GET.get('page')
    try:
        cars = all_car.page(page)
    except PageNotAnInteger:
        cars = all_car.page(1)
    except EmptyPage:
        cars = all_car.page(all_car.num_pages)
    name = Name.objects.all()
    first_registration = First_registration.objects.all()
    mileage = Mileage.objects.all()
    fuel = Fuel.objects.all()
    engine_size = Engine_size.objects.all()
    power = Power.objects.all()
    gearbox = Gearbox.objects.all()
    price = Price.objects.all()
    model = Car_model.objects.all()
    context = { 
                'qs':cars,
                'name':name,
                'first_registration':first_registration,
                'mileage':mileage,
                'fuel':fuel,
                'engine_size':engine_size,
                'power':power,
                'gearbox':gearbox,
                'price':price,
                'model':model,
                'nbar':'car_detail'
               }
    return render(request, 'cars.html', context)

class PostView(View):
    def get(self,request):
        posts = Post.objects.all()
        context = {
        'posts':posts,
        'nbar':'blog',
        }
        return render(request, 'blog.html', context)

class PostViewDetail(View):
    def get(self,request,post_slug):
        post = get_object_or_404(Post, slug=post_slug)
        context = {'post':post,}
        return render(request, 'blog_details.html', context)

class AddComment(View):
    def post(self,request,post_id):
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                create = form.save(commit=False)
                if request.POST.get("parent", None):
                    form.parent_id = int(request.POST.get('parent'))
                post = get_object_or_404(Post, id=post_id)
                create.post = post
                form.save()
                return HttpResponseRedirect(reverse("car:post_detail",kwargs = {"post_slug":post.slug}))
        else:
            form = CommentForm()
        return render(request,'blog_detail.html',{'form':form})

def contact(request):
    if request.method=='POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('car:home'))
        
        else:
            return HttpResponseRedirect(reverse('car:contact'))  
    else:
        form=ContactForm()
    return render(request,'contact.html', {'form':form,'nbar':'contact'})

def about(request):
    product = Product.objects.all()
    profile = Profile.objects.all()
    selled_products = product.filter(selled=True)
    return render(request,'about.html', {'product':product,'selled_products':selled_products,'profile':profile})

class FilterPostsView(ListView):
    model = Post
    template_name = 'list.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Post.objects.filter(
            Q(title__contains = query)
            )
        return object_list

def register_view(request):
    if request.user.is_authenticated:
        return redirect('car:profile')
    else:
        form = UserRegisterForm()
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                phone = request.POST.get('phone')
                Profile.objects.create(
                user=user,
                name=user.username,
                phone=phone,
                )
                messages.success(request, 'Yedi! '+username)
                return redirect('car:profile')
        context = {'form':form}
        return render(request, "account/signup.html", context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('car:profile')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('car:profile')
            else:
                messages.info(request, 'Username yoki passwordni xato kiritdingiz.')
        context={}
    return render(request, "account/login.html", context)

@login_required(login_url='car:login')
def logout_view(request):
    logout(request)
    return redirect('car:login')

@login_required(login_url='car:login')
def userpage(request):
    username = request.user.username
    if request.method=='GET':
        new = request.GET.get('new')
        car_type = request.GET.get('type')
        name = request.GET.get('name')
        year = request.GET.get('year')
        mileage = request.GET.get('mileage')
        fuel = request.GET.get('fuel')
        engine_size = request.GET.get('engine_size')
        power = request.GET.get('power')
        gearbox = request.GET.get('gearbox')
        color = request.GET.get('color')
        message = request.GET.get('desc')

        file = open("name.txt","w")
        file.write('Avtomobil Egasi  :    '+request.user.username+'\n\n')
        if new != None:
            if new == True:
                file.write('Avtomobil :  yangi\n\n')
            else:
                file.write('Avtomobil :  eski\n\n')
        if car_type != 'sellect' and car_type != None:
            file.write('Avtomobil turi :  '+car_type+'\n\n')
        if name != None:
            file.write('Avtomobil nomi :  '+name+'\n\n')
        if year != None:
            file.write('Avtomobil zavoddan chiqqan kuni :  '+year+'\n\n')
        if mileage != None:
            file.write('Avtomobil :  '+mileage+'km yurgan\n\n')
        if fuel != 'sellect' and car_type != None:
            file.write('Avtomobil :  '+fuel+'da yuradi\n\n')
        if engine_size != None:
            file.write('Avtomobil dvigatel hajmi :  '+engine_size+'\n\n')
        if power != None:
            file.write('Avtomobil quvvati :  '+power+'\n\n')
        if gearbox != None:
            file.write('Avtomobil vites qutisi :  '+gearbox+'\n\n')
        if color != None:
            file.write('Avtomobil rangi :  '+color+'\n\n')
        if message != None:
            file.write('Avtomobil matni :  '+message+'\n\n')
        file.close()
        with open("name.txt","rb") as text:
            f=text.read()
        if name != None:
            bot.sendMessage(my_id,f)

    return render(request, 'account/profile.html')