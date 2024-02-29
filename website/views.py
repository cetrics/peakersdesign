from re import sub
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
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from .forms import CommentForm




# Create your views here.
def home(request):

    context = {
        'services' : Service.objects.all(),
        'articles' : Article.objects.all()[:3],
        'projects' : Project.objects.all()
    }

    return render(request, 'index.html', context)

# Create your views here.
def contact(request):

    return render(request, 'contact.html', context={})

# Create your views here.
def about(request):

    return render(request, 'about.html', context={})

# Create your views here.
def articles(request):
    context = {
        'articles' : Article.objects.all(),
        'all_categories': Category.objects.all(),
        'title' : "All you can read buffet",            

    }

    return render(request,"articles.html", context )

# Create your views here.
def projects(request):
    context = {
        'articles' : Article.objects.all()[:3],
        'projects' : Project.objects.all(),     
    }

    return render(request,"projects.html", context )

def searchPosts(request):

    search = request.POST.get('searchInput', None)

    posts = Article.objects.filter(post__icontains= search).values()

    data ={
        'posts' : list(posts)
    }

    return JsonResponse(data)

def search(request):

    search = request.GET.get('search')

    posts = Article.objects.filter(post__icontains= search)

    context = {
        'articles' : posts,
        'all_categories': Category.objects.all(),
        'title' : "Posts matching:"+search,            

    }

    return render(request,"articles.html", context )

def getPostDetails(request, id):
    our_post = Article.objects.get(pk = id)

    # our_post.views += 1
    # our_post.save()

    # our_post.category.views +=1
    # our_post.category.save()
    
    context = {
        'post' : our_post,
        'categories' : Category.objects.all(),
        'articles' :  Article.objects.filter(category = our_post.category).exclude(pk = our_post.id),
        'commentForm' : CommentForm(),
        'comments' : Comment.objects.filter(article = our_post.id),
    }

    return render(request, 'post_details.html', context)

def saveComment(request, id):
    form = CommentForm(request.POST)
    redirect_url = "/articles/details/"+id


    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        user = User.objects.filter(email = email).first()

        if not user:
            user = User.objects.create_user(name, email, email)
        post = Article.objects.get(pk = id)

        Comment.objects.create(message = message, user = user, article = post)


        # return HttpResponseRedirect(redirect_url)
        return JsonResponse({'success': True})

    else:

        # return HttpResponseRedirect(redirect_url)
        return JsonResponse({'success': False})

def getCategoryPosts(request, id):

    category = Category.objects.get(pk = id)
    posts = Article.objects.filter(category = category.id)

    category.views +=1
    category.save()

    context = {
        'articles' : posts,
        'all_categories': Category.objects.all(),
        'title' : "Artcles in the category: "+ category.name,
    }

    return render(request, 'articles.html',context)

def saveFeedback(request):

    myname = request.POST.get("name", None)
    myemail = request.POST.get("email", None)
    no= request.POST.get("number", None)
    themessage = request.POST.get("message", None)

    # print(message)

    Feedback.objects.create(name= myname, email= myemail, phone_number = no, message = themessage)

    data = {}

    return JsonResponse(data)


def dashboard(request):

    articles = Article.objects.all()
    messages = Feedback.objects.all()
    

    context = {

        'recent_articles' : articles.order_by('id').reverse()[:5],
        'article_count' : articles.count(),
        'projects_count' : Project.objects.count(),
        'messages_count' : messages.count(),
        'feedback_list' : messages.filter(status = 0)[:2],
        'categories' : Category.objects.all(),
        'services' : Service.objects.all()

    }

    return render(request, 'admin/dashboard.html', context)

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

    context = {
        'success': True
    }

    return JsonResponse(context)


@login_required
def deleteService(request, id):

    service = Service.objects.get(pk = id)
    service.delete()

    context = {
        'success': True
    }

    return JsonResponse(context)

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


def mailStuff(request):

    if request.method == "GET":

        context = {
            'success' : 0
        }

        return JsonResponse(context)

    else:
        subject = request.POST["subject"]
        email = request.POST["recipient"]
        message = request.POST["message"]

        context = request.POST
        text_body = message
        html_body = render_to_string('admin/layouts/mail-template.html', context)

        mail = EmailMultiAlternatives(
            subject = subject,
            from_email = "brigeveriz7@gmail.com",
            to = [email],
            body = text_body
        )
        mail.attach_alternative(html_body, 'text/html')
        mail.send()

        data = {
            'success' : 1
        }

        return JsonResponse(data)
