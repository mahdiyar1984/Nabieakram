from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from blog_app.models import Article
from .forms import ArticleForm, TagForm
from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from account_app.models import User
from .forms import UserCreateForm, UserUpdateForm
from django.contrib.auth.models import Group



# region user & group management

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = "userprofile_app/users/user_list.html"

class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "userprofile_app/users/user_form.html"
    success_url = reverse_lazy('userprofile_app:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = Group.objects.all()
        return context

    def form_valid(self, form):
        form.instance.first_name = self.request.POST.get("first_name")
        form.instance.last_name = self.request.POST.get("last_name")
        form.instance.phone_number = self.request.POST.get("phone_number")
        form.instance.address = self.request.POST.get("address")
        form.instance.about_user = self.request.POST.get("about_user")

        if self.request.FILES.get("avatar"):
            form.instance.avatar = self.request.FILES["avatar"]

        response = super().form_valid(form)

        groups_ids = self.request.POST.getlist("groups")
        if groups_ids:
            self.object.groups.set(groups_ids)

        return response


class UserUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "userprofile_app/users/user_form.html"
    success_url = reverse_lazy('userprofile_app:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = Group.objects.all()
        return context

    def form_valid(self, form):
        form.instance.first_name = self.request.POST.get("first_name")
        form.instance.last_name = self.request.POST.get("last_name")
        form.instance.phone_number = self.request.POST.get("phone_number")
        form.instance.address = self.request.POST.get("address")
        form.instance.about_user = self.request.POST.get("about_user")

        if self.request.FILES.get("avatar"):
            form.instance.avatar = self.request.FILES["avatar"]

        response = super().form_valid(form)

        groups_ids = self.request.POST.getlist("groups")
        if groups_ids:
            self.object.groups.set(groups_ids)

        return response

class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = User
    template_name = "userprofile_app/users/user_confirm_delete.html"
    success_url = reverse_lazy('userprofile_app:user_list')


# endregion

# region Article management
class AuthorArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'userprofile_app/articles/article_list.html'

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user, is_delete=False)
class AuthorArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'userprofile_app/articles/article_form.html'
    success_url = reverse_lazy('userprofile_app:author_articles')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'tag_form' not in context:
            context['tag_form'] = TagForm()
        return context

    def post(self, request, *args, **kwargs):
        if "add_tag" in request.POST:
            tag_form = TagForm(request.POST)
            if tag_form.is_valid():
                tag_form.save()
            return redirect('userprofile_app:article_create')

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'draft'
        return super().form_valid(form)
class AuthorArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'userprofile_app/articles/article_form.html'
    success_url = reverse_lazy('author_articles')

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user, is_delete=False)
class AuthorArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'userprofile_app/articles/article_confirm_delete.html'
    success_url = reverse_lazy('author_articles')

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user, is_delete=False)

# endregion

# region setting
class UserPanelDashboardPage(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, template_name='userprofile_app/user_panel_dashboard_page.html')
class InformationUserProfile(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'userprofile_app/information_profile_user.html'

    def get_object(self, queryset=None):
        return self.request.user

class ArticleUserPanel(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'userprofile_app/articles/article_list.html'


    def get_queryset(self):
        return Article.objects.filter(user=self.request.user)

class EditUserProfilePage(LoginRequiredMixin, View):
    def get(self, request):
        return render(request,
                      template_name='userprofile_app/edit_profile_page.html',
                      context={'user': request.user})

    def post(self, request):
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.address = request.POST.get('address', '')
        user.phone_number = request.POST.get('phone_number','')
        user.about_user = request.POST.get('about_user')
        user.save()
        messages.success(request, 'تغییرات با موفقیت ثبت گردید')
        return redirect('userprofile_app:edit_user_profile_page')
class ChangePasswordPage(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, template_name='userprofile_app/change_password_page.html')

    def post(self, request):
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password1')
        confirm_password = request.POST.get('new_password2')

        if not old_password or not new_password or not confirm_password:
            messages.error(request, 'لطفاً همه فیلدها را پر کنید')
            return redirect('userprofile_app:change_password_page')

        user = request.user
        if not user.check_password(old_password):
            messages.error(request, 'کلمه عبور وارد شده اشتباه می باشد')
            return redirect('userprofile_app:change_password_page')

        if new_password != confirm_password:
            messages.error(request, 'کلمه عبور و تکرار کلمه عبور یکسان نیستند')
            return redirect('userprofile_app:change_password_page')

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'کلمه عبور با موفقیت تغییر یافت')
        return redirect('userprofile_app:user_panel_dashboard_page')
@login_required
def update_avatar(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        user = request.user
        user.avatar = request.FILES['avatar']
        user.save()
    return redirect('userprofile_app:user_panel_dashboard_page')
def user_panel_menu_component(request: HttpRequest):
    return render(request,
                  'userprofile_app/components/user_panel_menu_component.html')

# endregion