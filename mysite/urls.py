"""mysite URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from myapp import views
from myapp.views import ActivateAccount

urlpatterns = [
    path('admin/', admin.site.urls),
    url('Index/', views.Index, name='index'),
    url('Register/', views.Register, name='index'),
    url('Login/', views.Login, name='index'),
    url('Thanks/', views.Thanks, name='index'),
    url('CompleteProfile/', views.UserProfile, name='index'),
    url('Logout/',views.logout,name='logout'),
    url('handleRequest/', views.handlerequest, name='handle'),
    url('paymentMode/', views.paymentMode, name='handle'),
    url('MedicCall/', views.MedicApi, name='medic'),
    url('Daignosis/', views.Diagnosis, name='daignose'),
    #url('ProductShow/', views.pproducts, name='pp'),
    path('', include('myapp.urls')),
    #path('ProductShow/<int:id>',views.cart,name='cart'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
