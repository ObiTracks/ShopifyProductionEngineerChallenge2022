"""ShopifyProductionEngineerChallenge2022 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from app import views

urlpatterns = [
    path('admin', admin.site.urls),
    path('', views.dashboard, name="dashboard"),
    path('/<str:pk>', views.dashboard, name="load-instance"),

    # FORM HANDLER ENDPOINTS
    path('save/<str:pk>', views.saveInventory, name="save-inventory"),
    path('delete/<str:pk>', views.deleteInventory, name="delete-inventory"),

    #EXPORT HANDLER ENDPOINTS
    path('export/', views.export_all_inventories, name="export-inventories"),

    
]
