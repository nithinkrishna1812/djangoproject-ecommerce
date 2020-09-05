"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from store.views import home_page, cart_page, checkout_page, vegetable_page, fruits_page, homemade_products_page, natural_products_page, updateItem, processOrder, register_page, login_page, about_page, my_orders_page, deleteOrder, view_page
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home_page, name='home'),
    path('cart/', cart_page, name='cart'),
    path('vegetable/', vegetable_page, name='vegetables'),
    path('fruits/', fruits_page, name='fruits'),
    path('homemade_products/', homemade_products_page, name='homemade_products'),
    path('natural_products/', natural_products_page, name='natural_products'),
    path('view_products/<str:pk>/', view_page, name='view_products'),
    path('update_item/', updateItem, name='update_item'),
    path('process_order/', processOrder, name='process_order'),
    path('delete_order/<str:pk>/', deleteOrder, name='delete_order'),
    path('checkout/', checkout_page, name='checkout'),
    path('register/', register_page, name='register'),
    path('login/', login_page, name="login"),
    path('about/', about_page, name="about_page"),
    path('myorders/', my_orders_page, name="my_orders_page"),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
