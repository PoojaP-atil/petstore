"""
URL configuration for petstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from petapp.views import PetListView, PetDetailView, PetListViewCM
from django.conf import settings
from django.conf.urls.static import static
from petapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('petlist/',PetListView.as_view(), name='petlist'),
    path('petdetail/<slug:slug>/',PetDetailView.as_view(), name='petdetail'),
    path('petlistage/',PetListViewCM.as_view(),name='petlistage'),
    path('search/',views.searchbox, name='search'),
    path('register/',views.registration,name='register'),
    path('services/',views.services, name='services'),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('cart1/',views.addcart,name="cart"),
    path('viewcart/',views.viewcart,name="viewcart"),
    path('quantity/',views.quantity,name="quant"),
    path('summary/',views.summarypage,name="summary"),
    path('payment/',views.paymentpage,name="payment"),
    path('orderplaced/<str:tid>/<str:orderid>/', views.orderplaced, name='orderplaced'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)