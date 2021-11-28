from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['id','name',]
	list_display_links = ['name', ]
	prepopulated_fields = {'slug':('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ['id','title',]
	list_display_links = ['title', ]
	prepopulated_fields = {'slug':('title',)}
	
admin.site.register(Comment)
admin.site.register(Contact)

admin.site.register(Profile)
class ProductImageAdmin(admin.StackedInline):
	model =  ProductImages


@admin.register(Product)
class ProAdmin(admin.ModelAdmin):
	inlines = [ProductImageAdmin]
	list_display = ['name', 'category', 'selled']
	list_display_links = ['name', ]
	prepopulated_fields = {'slug':('name',)}

	class Meta:
		model = Product


@admin.register(ProductImages)
class PrImAdmin(admin.ModelAdmin):
	pass

@admin.register(Name)
class PNameAdmin(admin.ModelAdmin):
	pass

@admin.register(First_registration)
class PFRAdmin(admin.ModelAdmin):
	pass

@admin.register(Mileage)
class PMileageAdmin(admin.ModelAdmin):
	pass

@admin.register(Fuel)
class PFuelAdmin(admin.ModelAdmin):
	pass

@admin.register(Engine_size)
class PEngine_sizeAdmin(admin.ModelAdmin):
	pass

@admin.register(Power)
class PPowerAdmin(admin.ModelAdmin):
	pass

@admin.register(Gearbox)
class PGearboxAdmin(admin.ModelAdmin):
	pass

@admin.register(Old_price)
class Pold_priceAdmin(admin.ModelAdmin):
	pass

@admin.register(Price)
class PPriceAdmin(admin.ModelAdmin):
	pass

@admin.register(Car_model)
class PCar_modelAdmin(admin.ModelAdmin):
	pass