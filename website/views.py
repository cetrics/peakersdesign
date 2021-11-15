from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Feedback, Category, Article, Comment
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

    return render(request, "blog/admin/feedback.html", context)

@login_required
def showCategories(request):

    context = {
        'category_list' : Category.objects.all()
    }

    return render(request, "blog/admin/categories.html", context)

@login_required
def categoryForm(request):
    context = {}

    return render(request, "blog/admin/category_form.html", context)

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


class ArticleList(LoginRequiredMixin, ListView):
    model = Article
    template_name = "admin/articles.html"
    
@method_decorator(login_required, name="dispatch")
class ArticleCreate(CreateView):
    model = Article
    template_name = "admin/article_form.html"
    fields = ['title', 'message', 'slug', 'category', 'user', 'keywords', 'image_url']
    success_url = '/staff/articles'

    

@method_decorator(login_required, name="dispatch")
class ArticleDetails(DetailView):
    model = Article
    template_name = "blog/admin/article_details.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(post = self.kwargs['pk'])
        return context

@method_decorator(login_required, name="dispatch")
class ArticleUpdate(UpdateView):
    model = Article
    template_name = "blog/admin/article_form.html"
    fields = ['title', 'message', 'slug', 'category', 'user', 'keywords', 'image_url']
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

    return render(request, 'blog/blog.html',context)
    
def searchArticles(request):

    search = request.POST.get('searchInput', None)

    articles = Article.objects.filter(message__icontains= search).values()

    data ={
        'articles' : list(articles)
    }

    return JsonResponse(data)




