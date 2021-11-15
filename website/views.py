from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Feedback, Category, Article, Comment, Service, Seo, Project, ProjectWorker
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

# Create your views here.
def home(request):

    return render(request, 'index.html', context={})


def dashboard(request):

    return render(request, 'admin/dashboard.html', context={})

@login_required
def showFeedback(request):

    context = {}
    context['feedback_list'] = Feedback.objects.all()

    return render(request, "admin/feedback.html", context)

@login_required
def showCategories(request):

    context = {
        'categories' : Category.objects.all()
    }

    return render(request, "admin/categories.html", context)

@login_required
def categoryForm(request):
    context = {}

    return render(request, "admin/category_form.html", context)

@login_required
def storeCategory(request):

    category_name_from_form = request.POST.get("name")

    Category.objects.create(name = category_name_from_form)

    return HttpResponseRedirect('/staff/categories')

@login_required
def deleteCategory(request, id):

    our_category = Category.objects.get(pk = id)
    our_category.delete()

    return HttpResponseRedirect('/staff/categories')

@method_decorator(login_required, name="dispatch")
class ArticleList(LoginRequiredMixin, ListView):
    model = Article
    template_name = "admin/articles.html"
    
@method_decorator(login_required, name="dispatch")
class ArticleCreate(CreateView):
    model = Article
    template_name = "admin/article_form.html"
    fields = ['image_url', 'title', 'post', 'category', 'user', 'keywords']
    success_url = '/staff/articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Article'
        return context

    

@method_decorator(login_required, name="dispatch")
class ArticleDetails(DetailView):
    model = Article
    template_name = "admin/article_details.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(article = self.kwargs['pk'])
        return context

@method_decorator(login_required, name="dispatch")
class ArticleUpdate(UpdateView):
    model = Article
    template_name = "admin/article_form.html"
    fields = ['image_url', 'title', 'post', 'category', 'user', 'keywords']
    success_url = '/staff/articles'

def getCategoryArticles(request, id):

    category = Category.objects.get(pk = id)
    articles = Article.objects.filter(category = category.id)

    category.views +=1
    category.save()

    context = {
        'articles' : articles,
        'all_categories': Category.objects.all(),
        'title' : "Articles in the category: "+ category.name,
    }

    return render(request, 'blog.html',context)
    
def searchArticles(request):

    search = request.POST.get('searchInput', None)

    articles = Article.objects.filter(message__icontains= search).values()

    data ={
        'articles' : list(articles)
    }

    return JsonResponse(data)


###Services
@method_decorator(login_required, name="dispatch")
class ServiceList(LoginRequiredMixin, ListView):
    model = Service
    context_object_name = 'services'
    template_name = "admin/services.html"

@method_decorator(login_required, name="dispatch")
class ServiceCreate(CreateView):
    model = Service
    template_name = "admin/layouts/default_form.html"
    fields = ['icon','name', 'description']
    success_url = '/staff/services'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Service'
        return context

@method_decorator(login_required, name="dispatch")
class ServiceDetails(DetailView):
    model = Service
    template_name = "admin/service_details.html"
    context_object_name = "services"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = Project.objects.filter(service = self.kwargs['pk'])
        return context

@method_decorator(login_required, name="dispatch")
class ServiceUpdate(UpdateView):
    model = Service
    template_name = "admin/layouts/default_form.html"
    fields = ['name', 'description', 'icon']
    success_url = '/staff/services'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Service'
        return context

###Projects
@method_decorator(login_required, name="dispatch")
class ProjectList(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = 'projects'
    template_name = "admin/projects.html"

@method_decorator(login_required, name="dispatch")
class ProjectCreate(CreateView):
    model = Project
    template_name = "admin/layouts/default_form.html"
    fields = ['image_url','title', 'description', 'keywords', 'service']
    success_url = '/staff/projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Project'
        return context

@method_decorator(login_required, name="dispatch")
class ProjectDetails(DetailView):
    model = Project
    template_name = "admin/project_details.html"
    context_object_name = "project"

@method_decorator(login_required, name="dispatch")
class ProjectUpdate(UpdateView):
    model = Project
    template_name = "admin/layouts/default_form.html"
    fields = ['image_url','title', 'description', 'keywords', 'service']
    success_url = '/staff/projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Project'
        return context

def seo(request):

    return render(request, 'admin/seo.html', context={})




