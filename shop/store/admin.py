from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe

# Register your models here.
class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'get_products_count')
    prepopulated_fields = {'slug': ('title',)}

    def get_products_count(self, obj):
        if obj.products:
            return str(len(obj.products.all()))
        else:
            return '0'

    get_products_count.short_description = 'Product quantity'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'price', 'quantity', 'product_size', 'created_at')
    list_editable = ('price', 'quantity', 'product_size')
    list_display_links = ('title', )
    prepopulated_fields = {'slug': ('title', )}
    list_filter = ('title', 'price', 'product_size')
    inlines = [GalleryInline]

    # Данные метод поможет увидить картинку в админке
    def get_photo(self, obj):
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width="75">')
            except:
                return '-'
        else:
            return '-'

    get_photo.short_description = 'Product photo'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text', 'product', 'created_at')
    readonly_fields = ('author', 'text', 'created_at')


@admin.register(ShippingAddresses)
class ShippingAddressesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'customer', 'order', 'address', 'city', 'state', 'phone', 'created_at')
    readonly_fields = ('customer', 'order', 'address', 'city', 'state', 'phone')


# -------------------------------------------------------------------------------------------------------
admin.site.register(Gallery)
admin.site.register(FavouriteProducts)
admin.site.register(Mail)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(City)
