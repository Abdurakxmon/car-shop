from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse


class Categories(models.Model):
	name = models.CharField(max_length=50)
	slug = models.SlugField(max_length=50, unique=True, db_index=True)

	def __str__(self):
		return f"Category - {self.name}"

	class Meta:
		verbose_name = 'Category'
		verbose_name_plural = 'Categorys'



class Name(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class First_registration(models.Model):
	first_registration = models.CharField(max_length=50)

	def __str__(self):
		return self.first_registration

class Mileage(models.Model):
	mileage = models.CharField(max_length=50)

	def __str__(self):
		return self.mileage

class Fuel(models.Model):
	fuel = models.CharField(max_length=50)

	def __str__(self):
		return self.fuel

class Engine_size(models.Model):
	engine_size = models.CharField(max_length=50)

	def __str__(self):
		return self.engine_size

class Power(models.Model):
	power = models.CharField(max_length=50)

	def __str__(self):
		return self.power

class Gearbox(models.Model):
	gearbox = models.CharField(max_length=50)

	def __str__(self):
		return self.gearbox

class Old_price(models.Model):
	old_price = models.CharField(max_length=50)

	def __str__(self):
		return self.old_price
class Price(models.Model):
	price = models.CharField(max_length=50)

	def __str__(self):
		return self.price
class Car_model(models.Model):
	model = models.CharField(max_length=50)

	def __str__(self):
		return self.model

class Profile(models.Model):
	user = models.OneToOneField(User,blank=True,null=True, on_delete=models.CASCADE, related_name='user_profile',)
	name = models.CharField(max_length=50, null=True)
	phone= models.CharField(max_length=50,null=True)
	poster = models.ImageField(upload_to='users/poster', default='static/user.jpg')

	def __str__(self):
		return f'user - {self.user.username}'

class Product(models.Model):
	CHOICES = (
		('white','WHITE'),
		('black','BLACK'),
		('blue','BLUE'),
		('green','GREEN'),
		('yellow','YELLOW'),
		('red','RED'),
		)

	new = models.BooleanField(default=False)
	name = models.ForeignKey(Name,on_delete=models.CASCADE,default=True)
	slug = models.SlugField('*', unique=True)
	model = models.ForeignKey(Car_model,on_delete=models.CASCADE,default=True, null=True)
	category = models.ForeignKey(Categories, on_delete=models.CASCADE,default=True)
	first_registration = models.ForeignKey(First_registration,on_delete=models.CASCADE,default=True)
	mileage = models.ForeignKey(Mileage,on_delete=models.CASCADE,default=True)
	fuel = models.ForeignKey(Fuel,on_delete=models.CASCADE,default=True)
	engine_size = models.ForeignKey(Engine_size,on_delete=models.CASCADE,default=True)
	power = models.ForeignKey(Power,on_delete=models.CASCADE,default=True)
	gearbox = models.ForeignKey(Gearbox,on_delete=models.CASCADE,default=True)
	image = models.ImageField(upload_to="car_images/")
	vehicle_description = RichTextField(blank=True)
	vehicle_extras = RichTextField()
	old_price = models.ForeignKey(Old_price,on_delete=models.CASCADE,default=True)
	price = models.ForeignKey(Price,on_delete=models.CASCADE,default=True)
	colors = models.CharField(max_length=50, choices=CHOICES,default=True )
	contact_detail = models.ForeignKey(Profile, on_delete=models.CASCADE,default=True)
	selled = models.BooleanField()

	class Meta:
		verbose_name = 'Car'
		verbose_name_plural = 'Cars'

	def get_absolute_url(self):
		return reverse('car:product_detail', kwargs={'car_slug':self.slug})

	def __str__(self):
		return f"Car - {self.name}"


class ProductImages(models.Model):
	product = models.ForeignKey(Product,default=None, blank=True, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='product_images/', blank=True)

	class Meta:
		verbose_name = 'Image'
		verbose_name_plural = 'Images'


class Post(models.Model):
	title = models.CharField(max_length=550)
	slug = models.SlugField('*',max_length=150, unique=True, db_index=True)
	body = RichTextField()
	image = models.ImageField(upload_to='blog_images/')
	author = models.CharField( max_length=50, blank=True, default='Admin')
	published = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Post - {self.title}"

	def get_absolute_url(self):
		return reverse('car:post_detail', kwargs={'post_slug':self.slug})

	class Meta:
		verbose_name = 'Post'
		verbose_name_plural = 'Posts'


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='post_comments', null=True)
	name = models.CharField( max_length=50, null=True)
	email = models.EmailField(max_length=50,blank=True)
	message	= models.TextField(null=True)
	date = models.DateTimeField(auto_now_add=True, null=True)
	parent = models.ForeignKey('self',verbose_name = 'parent',on_delete=models.SET_NULL,null=True,blank = True)

	class Meta:
		verbose_name='comment'
		verbose_name_plural='comments'
	def __str__(self):
		return self.name


class Contact(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField(max_length=224)
	title = models.CharField(max_length=150,default=True)
	message = models.TextField()

	class Meta:
		verbose_name = 'Contact'
		verbose_name_plural = 'Contacts'

	def __str__(self):
		return f"Message - {self.name}"


