from django.urls import path
from .views import *
from . import views



urlpatterns = [
    path('', ProductList.as_view(), name='product_list'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category_detail'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),

    path('registration/', registration, name='registration'),
    path('login/', sign_in, name='sign_in'),

    path('user_logout', user_logout, name='logout'),
    path('user_login', user_login, name='login'),
    path('register', register, name='register'),

    path('save_review/<int:product_id>', save_review, name='save_review'),
    path('add_favourite/<slug:product_slug>/', save_favourite_product, name='add_favourite'),
    path('my_favourite', FavouriteProductsView.as_view(), name='favourite_products'),
    path('subscription/', subscription, name='sub'),
    path('save_mail/', save_mail, name='save_mail'),
    path('send_mail/', send_mail_to_customer, name='send_mail'),

    path('cart/', cart, name='cart'),
    path('to_cart/<int:product_id>/<str:action>/', to_cart, name='to_cart'),
    path('checkout/', checkout, name='checkout'),

    path('payment/', create_checkout_session, name='payment'),
    path('payment_success/', success_payment, name='success'),
    path('clear_cart/', clear2, name='clear_cart'),

    path('profile/', views.user_profile, name='user_profile'),  # New URL for the user profile
]