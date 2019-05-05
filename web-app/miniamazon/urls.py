"""miniamazon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,include
from browsePro.views import homepage
from django.contrib.auth.decorators import login_required
from users.views import index_login,index_register,djlogout
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homepage,name = 'homepage'),
    path('logout/',djlogout,name = 'logout'),
    path('login/',index_login,name = 'login'),
    path('signup/',index_register,name = 'signup'),
    path('browsePro/',include('browsePro.urls')),
    path('mycarts/',include('cart.urls')),
    path('checkorder/',include('order.urls'))
]
