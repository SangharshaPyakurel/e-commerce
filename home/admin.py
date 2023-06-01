from django.contrib import admin

from home.models import *

# Register your models here.
# admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Slider)
admin.site.register(Ad)
admin.site.register(Brand)
# admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Contact)
admin.site.register(ProductReview)
admin.site.register(Cart)

#customize django admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price","stock","labels","category","subcategory","brand")
    search_fields = ["name", "description"]
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "logo","slug")