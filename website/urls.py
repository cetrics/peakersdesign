"""peakers_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
from .views import *


staffpatterns = [

    path("dashboard", dashboard, name="dashboard"),
    path('feedback', showFeedback, name="feedback"),
    path('categories', showCategories, name="categories"),
    path('category/form', categoryForm, name="add_category"),
    path('store/category', storeCategory, name="store_category"),
    path('delete/category/<id>',deleteCategory, name="delete_category"),

    ##articles
    path('articles', ArticleList.as_view(), name="articles"),
    path('create/article', ArticleCreate.as_view(), name="add_article"),
    path('view/articles/<pk>', ArticleDetails.as_view(), name="view_article"),
    path('update/articles/<pk>', ArticleUpdate.as_view(), name="update_article"),

    ##services
    path('services', ServiceList.as_view(), name="services"),
    path('create/service',ServiceCreate.as_view(), name="add_service"),
    path('view/services/<pk>', ServiceDetails.as_view(), name="view_service"),
    path('update/services/<pk>', ServiceUpdate.as_view(), name="update_service"),

    ##projects
    path('projects', ProjectList.as_view(), name="projects"),
    path('create/project',ProjectCreate.as_view(), name="add_project"),
    path('view/project/<pk>', ProjectDetails.as_view(), name="view_project"),
    path('update/project/<pk>', ProjectUpdate.as_view(), name="update_project"),

    path('seo', seo, name="seo")

]

urlpatterns = [
    path("", home, name="home"),
    path("contact", home, name="contact"),
    path("articles", home, name="articles"),
    path("portfolio", home, name="portfolio"),
    path("request/quote", home, name="request.quote"),
    path("staff/", include(staffpatterns))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
