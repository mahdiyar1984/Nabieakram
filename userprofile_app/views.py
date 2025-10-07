from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.views.generic import DetailView, TemplateView
from blog_app.models import Article, ArticleCategory, ArticleTag, ArticleComment
from main_app.models import FooterLink, ContactUs, SiteSetting, Slider
from media_app.models import Lecture, LectureCategory, LectureTag, LectureComment, GalleryImage, GalleryCategory, BaseModel
from .forms import ArticleForm, GroupForm, ArticleCategoryForm, ArticleTagForm, LectureForm, LectureTagForm, \
    LectureCategoryForm, GalleryImageForm, \
    GalleryCategoryForm, FooterLinkForm, ContactUsForm, SliderForm, SiteSettingForm
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from account_app.models import User
from .forms import UserCreateForm, UserUpdateForm
from django.contrib.auth.models import Group, Permission
from django.apps import apps


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


# region dashboard
class UserPanelDashboardPage(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, template_name='userprofile_app/dashboard/user_panel_dashboard_page.html')


# endregion

# region Groups
class GroupPermissionMatrixView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = "userprofile_app/groups/groups_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        groups = Group.objects.all()
        actions = ["add", "change", "delete", "view"]

        apps_dict = {}
        for perm in Permission.objects.all().select_related("content_type"):
            app_label = perm.content_type.app_label
            model_name = perm.content_type.model  # lowercase مثل articlecategory

            app_config = apps.get_app_config(app_label)
            app_verbose = app_config.verbose_name.title()

            model_class = apps.get_model(app_label, model_name)
            model_verbose = model_class._meta.verbose_name.title()

            codename = perm.codename

            if app_verbose not in apps_dict:
                apps_dict[app_verbose] = {}

            if model_name not in apps_dict[app_verbose]:
                apps_dict[app_verbose][model_name] = {
                    "verbose": model_verbose,
                    "perms": []
                }

            apps_dict[app_verbose][model_name]["perms"].append(codename)

        for group in groups:
            group.codename_list = set(group.permissions.values_list("codename", flat=True))

        context.update({
            "groups": groups,
            "actions": actions,
            "apps_dict": apps_dict,
        })
        return context

    def post(self, request, *args, **kwargs):
        groups = Group.objects.all()
        all_perms = Permission.objects.all()
        perm_map = {p.codename: p for p in all_perms}  # دیکشنری برای دسترسی سریع

        for group in groups:
            selected_codenames = request.POST.getlist(f'permissions_{group.id}[]')

            # گرفتن لیست پرمیشن‌ها از دیکشنری به صورت سریع
            selected_perms = [perm_map[c] for c in selected_codenames if c in perm_map]

            # جایگزینی پرمیشن‌ها به صورت bulk
            group.permissions.set(selected_perms)

        return redirect(request.path)


class GroupCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = "userprofile_app/groups/group_form.html"
    success_url = reverse_lazy("group_list")


class GroupUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = "userprofile_app/groups/group_form.html"
    success_url = reverse_lazy("group_list")


class GroupDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Group
    template_name = "userprofile_app/groups/group_confirm_delete.html"
    success_url = reverse_lazy("group_list")


# endregion

# region user
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
        # فیلدهای پایه
        form.instance.first_name = self.request.POST.get("first_name")
        form.instance.last_name = self.request.POST.get("last_name")
        form.instance.phone_number = self.request.POST.get("phone_number")
        form.instance.address = self.request.POST.get("address")
        form.instance.about_user = self.request.POST.get("about_user")

        if self.request.FILES.get("avatar"):
            form.instance.avatar = self.request.FILES["avatar"]

        # ذخیره superuser فقط اگر کاربر جاری superuser باشد
        if self.request.user.is_superuser:
            form.instance.is_superuser = self.request.POST.get("is_superuser") == "on"

        response = super().form_valid(form)

        # ذخیره گروه‌ها
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
        # فیلدهای پایه
        form.instance.first_name = self.request.POST.get("first_name")
        form.instance.last_name = self.request.POST.get("last_name")
        form.instance.phone_number = self.request.POST.get("phone_number")
        form.instance.address = self.request.POST.get("address")
        form.instance.about_user = self.request.POST.get("about_user")

        if self.request.FILES.get("avatar"):
            form.instance.avatar = self.request.FILES["avatar"]

        # ذخیره superuser فقط اگر کاربر جاری superuser باشد
        if self.request.user.is_superuser:
            form.instance.is_superuser = self.request.POST.get("is_superuser") == "on"

        response = super().form_valid(form)

        # ذخیره گروه‌ها
        groups_ids = self.request.POST.getlist("groups")
        if groups_ids:
            self.object.groups.set(groups_ids)

        return response


class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = User
    template_name = "userprofile_app/users/user_confirm_delete.html"
    success_url = reverse_lazy('userprofile_app:user_list')


# endregion

# region Article
class AdminArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'userprofile_app/articles/articles_list.html'
    paginate_by = 10


class AdminArticleReadView(LoginRequiredMixin, DetailView):
    model = Article
    form_class = ArticleForm
    template_name = "userprofile_app/articles/article_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ArticleForm(instance=self.get_object(), read_only=True)
        context['read_only'] = getattr(context.get('form'), 'read_only', True)
        context['tags'] = ArticleTag.objects.all()
        context['categories'] = ArticleCategory.objects.all()
        return context


class AdminArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'userprofile_app/articles/article_form.html'
    success_url = reverse_lazy('userprofile_app:articles_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ArticleCategory.objects.all()
        context['tags'] = ArticleTag.objects.all()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.status = 'draft'

        # استفاده از فرم برای فایل
        if form.cleaned_data.get('image'):
            self.object.image = form.cleaned_data['image']

        self.object.save()

        # ذخیره ManyToMany از فرم (اعتبارسنجی شده)
        if 'selected_categories' in form.cleaned_data:
            self.object.selected_categories.set(form.cleaned_data['selected_categories'])
        if 'selected_tags' in form.cleaned_data:
            self.object.selected_tags.set(form.cleaned_data['selected_tags'])

        return super().form_valid(form)


class AdminArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'userprofile_app/articles/article_form.html'
    success_url = reverse_lazy('userprofile_app:articles_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ArticleCategory.objects.all()
        context['tags'] = ArticleTag.objects.all()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user

        # آپلود تصویر جدید
        if self.request.FILES.get('image'):
            self.object.image = self.request.FILES['image']

        # وضعیت پیش‌فرض
        if self.object.status in ['rejected', 'draft', 'pending']:
            self.object.status = 'draft'

        self.object.save()

        # ذخیره ManyToMany
        self.object.selected_categories.set(form.cleaned_data['selected_categories'])
        self.object.selected_tags.set(form.cleaned_data['selected_tags'])

        return super().form_valid(form)


class AdminArticleDeleteView(LoginRequiredMixin, View):
    success_url = reverse_lazy('userprofile_app:articles_list')

    def post(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk, author=request.user)
        article.is_delete = True
        article.save()
        return redirect(self.success_url)


class AdminArticleChangeStatusView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        action = request.POST.get("action")

        # if author wants to do pending in himself article
        if action == "submit_for_review" and article.author == request.user:
            article.status = "pending"
            article.save()
            messages.success(request, "مقاله برای بررسی ارسال شد.")
            return redirect("userprofile_app:articles_list")

        # if editor or admin wants to confirm the article
        if action == "publish" and request.user.has_perm("blog_app.can_publish_article"):
            article.status = "published"
            article.save()
            messages.success(request, "مقاله منتشر شد.")
            return redirect("userprofile_app:articles_list")

        # if editor or admin wants to reject the article
        if action == "reject" and request.user.has_perm("blog_app.can_reject_article"):
            article.status = "rejected"
            article.save()
            messages.warning(request, "مقاله رد شد.")
            return redirect("userprofile_app:articles_list")

        messages.error(request, "شما اجازه این کار را ندارید.")
        return redirect("userprofile_app:articles_list")


# endregion
# region Article Category
class AdminArticleCategoryListView(LoginRequiredMixin, ListView):
    model = ArticleCategory
    template_name = 'userprofile_app/articles/article_categories_list.html'
    paginate_by = 10


def article_category_create_view(request, pk=None):
    obj = get_object_or_404(ArticleCategory, pk=pk) if pk else None
    if request.method == "POST":
        form = ArticleCategoryForm(request.POST, request.FILES)
        if form.is_valid():  # اعتبارسنجی فرم انجام می‌شود
            data = form.cleaned_data
            if obj:
                article_category = obj
            else:
                article_category = ArticleCategory()

            # مقداردهی فیلدها
            article_category.title = data['title']
            article_category.url_title = data['url_title']
            article_category.parent = data.get('parent')
            article_category.is_active = data.get('is_active', False)
            article_category.is_delete = data.get('is_delete', False)

            if data.get('image'):
                article_category.image = data['image']

            article_category.save()
            return redirect('userprofile_app:article_categories_list')  # آدرس صفحه موفقیت

    else:
        # GET request → پر کردن فرم با مقادیر اولیه برای ویرایش یا فرم خالی
        initial = {}
        if obj:
            initial = {
                'title': obj.title,
                'url_title': obj.url_title,
                'parent': obj.parent,
                'is_active': obj.is_active,
                'is_delete': obj.is_delete
            }
        form = ArticleCategoryForm(initial=initial)

        # همه دسته‌بندی‌ها برای select والد

    all_categories = ArticleCategory.objects.all()

    return render(request, 'userprofile_app/articles/article_category_form.html', {
        'form': form,
        'object': obj,
        'all_categories': all_categories,
        'read_only': False
    })


def article_category_update_view(request, pk):
    # بارگذاری شیء موجود
    article_category = get_object_or_404(ArticleCategory, pk=pk)

    if request.method == "POST":
        form = ArticleCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            # به‌روزرسانی فیلدها
            article_category.title = data['title']
            article_category.url_title = data['url_title']
            article_category.parent = data.get('parent')
            article_category.is_active = 'is_active' in request.POST
            article_category.is_delete = 'is_delete' in request.POST

            if data.get('image'):
                article_category.image = data['image']

            article_category.save()
            return redirect('userprofile_app:article_categories_list')

    else:
        # پر کردن فرم با مقادیر فعلی شیء
        initial = {
            'title': article_category.title,
            'url_title': article_category.url_title,
            'parent': article_category.parent,
            'is_active': article_category.is_active,
            'is_delete': article_category.is_delete
        }
        form = ArticleCategoryForm(initial=initial)

    all_categories = ArticleCategory.objects.all()

    return render(request, 'userprofile_app/articles/article_category_form.html', {
        'form': form,
        'object': article_category,
        'all_categories': all_categories,
        'read_only': False
    })


def article_category_read_view(request, pk):
    article_category = get_object_or_404(ArticleCategory, pk=pk)
    initial = {
        'title': article_category.title,
        'url_title': article_category.url_title,
        'parent': article_category.parent,
        'is_active': article_category.is_active,
        'is_delete': article_category.is_delete
    }

    # فرم با مقادیر اولیه
    form = ArticleCategoryForm(initial=initial)

    # اگر read_only باشد، همه فیلدها غیرفعال می‌شوند
    read_only = True
    if read_only:
        for field in form.fields.values():
            field.widget.attrs['disabled'] = True

    all_categories = ArticleCategory.objects.all()

    return render(request, 'userprofile_app/articles/article_category_form.html', {
        'form': form,
        'object': article_category,
        'all_categories': all_categories,
        'read_only': read_only
    })


def article_category_delete_view(request, pk):
    if request.method == 'POST':
        article_category = get_object_or_404(ArticleCategory, pk=pk)
        article_category.is_delete = True
        article_category.save()
    return redirect('userprofile_app:article_categories_list')


# endregion
# region Article Tag
class AdminArticleTagListView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        article_tags: QuerySet[ArticleTag] = ArticleTag.objects.all().order_by('id')
        paginator = Paginator(article_tags, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj,
        }
        return render(request, 'userprofile_app/articles/article_tags_list.html', context)


class AdminArticleTagReadView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, pk):
        article_tag: ArticleTag = get_object_or_404(ArticleTag, pk=pk)
        article_tag_form = ArticleTagForm(instance=article_tag, read_only=True)
        context = {
            'article_tag_form': article_tag_form,
        }
        return render(request, 'userprofile_app/articles/article_tag_form.html', context)


class AdminArticleTagCreateView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        article_tag_form = ArticleTagForm()
        context = {
            'article_tag_form': article_tag_form,
        }
        return render(request, 'userprofile_app/articles/article_tag_form.html', context)

    def post(self, request: HttpRequest):
        article_tag_form = ArticleTagForm(request.POST)
        if article_tag_form.is_valid():
            article_tag_form.save()
            messages.success(request, "تگ با موفقیت ایجاد شد ✅")
            return redirect('userprofile_app:article_tags_list')
        else:
            messages.error(request, "خطا در ثبت فرم ❌ لطفاً فیلدها را بررسی کنید.")


class AdminArticleTagUpdateView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, pk):
        article_tag: ArticleTag = get_object_or_404(ArticleTag, pk=pk)
        article_tag_form = ArticleTagForm(instance=article_tag)
        context = {
            'article_tag_form': article_tag_form,
        }
        return render(request, 'userprofile_app/articles/article_tag_form.html', context)

    def post(self, request: HttpRequest, pk):
        article_tag: ArticleTag = get_object_or_404(ArticleTag, pk=pk)
        article_tag_form = ArticleTagForm(request.POST, instance=article_tag)
        if article_tag_form.is_valid():
            article_tag_form.save()
            messages.success(request, "تگ با موفقیت ایجاد شد ✅")
            return redirect('userprofile_app:article_tags_list')
        else:
            messages.error(request, "خطا در ثبت فرم ❌ لطفاً فیلدها را بررسی کنید.")


class AdminArticleTagDeleteView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, pk):
        article_tag: ArticleTag = get_object_or_404(ArticleTag, pk=pk)
        article_tag.is_delete = True
        article_tag.save()
        return redirect('userprofile_app:article_tags_list')


# endregion
# region Article Comment

@staff_member_required
def admin_article_comment_list(request: HttpRequest):
    article_comments: QuerySet[ArticleComment] = (
        ArticleComment.objects
        .select_related('article', 'user')
        .prefetch_related('articlecomment_set__user')
        .filter(parent__isnull=True)
        .order_by('-create_date')
    )
    paginator = Paginator(article_comments, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, template_name='userprofile_app/articles/article_comments_list.html', context=context)


@staff_member_required
def admin_article_comment_read(request: HttpRequest, pk):
    comment: ArticleComment = ArticleComment.objects.get(pk=pk)
    context = {
        'comment': comment,
        'read_only': True
    }
    return render(request, 'userprofile_app/articles/article_comment_form.html', context)


@staff_member_required
def admin_article_comment_update(request: HttpRequest, pk):
    comment: ArticleComment = ArticleComment.objects.get(pk=pk)
    if request.method == 'POST':
        comment.text = request.POST.get('text', comment.text)
        comment.is_active = 'is_active' in request.POST
        comment.is_delete = 'is_delete' in request.POST
        comment.save()
        reply_text = request.POST.get('reply_text')
        if reply_text:
            first_reply = comment.articlecomment_set.first()
            if first_reply:
                first_reply.text = reply_text
                first_reply.save()
            else:
                ArticleComment.objects.create(
                    article=comment.article,
                    user=request.user,
                    parent=comment,
                    text=reply_text
                )

        return redirect('userprofile_app:article_comments_list')

    context = {'comment': comment, 'read_only': False}
    return render(request, 'userprofile_app/articles/article_comment_form.html', context)


def admin_article_comment_delete(request: HttpRequest, pk):
    comment: ArticleComment = ArticleComment.objects.get(pk=pk)
    comment.is_delete = True
    comment.save()
    return redirect('userprofile_app:article_comments_list')


# endregion

# region Lecture
class AdminLectureListView(LoginRequiredMixin, ListView):
    model = Lecture
    template_name = 'userprofile_app/lectures/lectures_list.html'
    paginate_by = 5


class AdminLectureReadView(LoginRequiredMixin, DetailView):
    model = Lecture
    form_class = LectureForm
    template_name = "userprofile_app/lectures/lecture_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LectureForm(instance=self.get_object(), read_only=True)
        context['read_only'] = getattr(context.get('form'), 'read_only', True)
        context['categories'] = LectureCategory.objects.all()
        context['tags'] = LectureTag.objects.all()
        return context


class AdminLectureCreateView(LoginRequiredMixin, CreateView):
    model = Lecture
    form_class = LectureForm
    template_name = 'userprofile_app/lectures/lecture_form.html'
    success_url = reverse_lazy('userprofile_app:lectures_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = LectureCategory.objects.all()
        context['tags'] = LectureTag.objects.all()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        form.save_m2m()
        return redirect(self.get_success_url())


class AdminLectureUpdateView(LoginRequiredMixin, UpdateView):
    model = Lecture
    form_class = LectureForm
    template_name = 'userprofile_app/lectures/lecture_form.html'
    success_url = reverse_lazy('userprofile_app:lectures_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = LectureCategory.objects.all()
        context['tags'] = LectureTag.objects.all()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        form.save_m2m()
        return redirect(self.get_success_url())


class AdminLectureDeleteView(LoginRequiredMixin, DeleteView):
    model = Lecture
    template_name = 'userprofile_app/lectures/lecture_category_confirm_delete.html'
    success_url = reverse_lazy('userprofile_app:articles_list')

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user, is_delete=False)


class AdminlectureChangeStatusView(LoginRequiredMixin, View):
    pass


# endregion
# region Lecture Category
class AdminLectureCategoryListView(LoginRequiredMixin, ListView):
    model = LectureCategory
    template_name = 'userprofile_app/lectures/lecture_categories_list.html'

    def get_queryset(self):
        return LectureCategory.objects.filter(is_delete=False)


class AdminLectureCategoryCreateView(LoginRequiredMixin, CreateView):
    model = LectureCategory
    form_class = LectureCategoryForm
    template_name = 'userprofile_app/lectures/lecture_category_form.html'
    success_url = reverse_lazy('userprofile_app:lecture_categories_list')


class AdminLectureCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = LectureCategory
    form_class = LectureCategoryForm
    template_name = 'userprofile_app/lectures/lecture_category_form.html'
    success_url = reverse_lazy('userprofile_app:lecture_categories_list')


class AdminLectureCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = LectureCategory
    template_name = 'userprofile_app/lectures/lecture_category_confirm_delete.html'
    success_url = reverse_lazy('userprofile_app:lecture_categories_list')


# endregion
# region Lecture Tag
class AdminLectureTagListView(LoginRequiredMixin, ListView):
    model = LectureTag
    template_name = 'userprofile_app/lectures/lecture_tags_list.html'

    def get_queryset(self):
        return LectureTag.objects.filter(is_delete=False)


class AdminLectureTagCreateView(LoginRequiredMixin, CreateView):
    model = LectureTag
    form_class = LectureTagForm
    template_name = 'userprofile_app/lectures/lecture_tag_form.html'
    success_url = reverse_lazy('userprofile_app:lecture_tags_list')


class AdminLectureTagUpdateView(LoginRequiredMixin, UpdateView):
    model = LectureTag
    form_class = LectureTagForm
    template_name = 'userprofile_app/lectures/lecture_tag_form.html'
    success_url = reverse_lazy('userprofile_app:lecture_tags_list')


class AdminLectureTagDeleteView(LoginRequiredMixin, DeleteView):
    model = LectureTag
    template_name = 'userprofile_app/lectures/lecture_tag_confirm_delete.html'
    success_url = reverse_lazy('userprofile_app:lecture_tags_list')


# endregion
# region Lecture Comment
class AdminLectureCommentListView(LoginRequiredMixin, ListView):
    model = LectureComment
    template_name = 'userprofile_app/lectures/lecture_comments_list.html'

    def get_queryset(self):
        return LectureTag.objects.filter(is_delete=False)


class AdminLectureCommentCreateView(LoginRequiredMixin, CreateView):
    model = LectureTag
    form_class = LectureTagForm
    template_name = 'userprofile_app/lectures/lecture_comment_form.html'
    success_url = reverse_lazy('userprofile_app:lecture_comment_list')


class AdminLectureCommentUpdateView(LoginRequiredMixin, UpdateView):
    model = LectureTag
    form_class = LectureTagForm
    template_name = 'userprofile_app/lectures/lecture_comment_form.html'
    success_url = reverse_lazy('userprofile_app:lecture_comment_list')


class AdminLectureCommentDeleteView(LoginRequiredMixin, DeleteView):
    model = LectureTag
    template_name = 'userprofile_app/lectures/lecture_comment_confirm_delete.html'
    success_url = reverse_lazy('userprofile_app:lecture_comment_list')


# endregion

# region Gallery
class AdminGalleryImageListView(LoginRequiredMixin, ListView):
    model = GalleryImage
    template_name = 'userprofile_app/galleries/galleries_list.html'

    def get_queryset(self):
        return GalleryImage.objects.filter(is_delete=False)


class AdminGalleryImageCreateView(LoginRequiredMixin, CreateView):
    pass


class AdminGalleryImageUpdateView(LoginRequiredMixin, UpdateView):
    model = GalleryImage
    form_class = GalleryImageForm
    template_name = 'userprofile_app/galleries/gallery_form.html'
    success_url = reverse_lazy('userprofile_app:galleries_list')

    def get_queryset(self):
        return GalleryImage.objects.filter(is_delete=False)


class AdminGalleryImageDeleteView(LoginRequiredMixin, DeleteView):
    model = GalleryImage
    template_name = 'userprofile_app/galleries/gallery_category_confirm_delete.html'
    success_url = reverse_lazy('userprofile_app:galleries_list')

    def get_queryset(self):
        return GalleryImage.objects.filter(is_delete=False)


# endregion
# region Gallery Category
class AdminGalleryCategoryListView(LoginRequiredMixin, ListView):
    model = GalleryCategory
    template_name = 'userprofile_app/galleries/gallery_categories_list.html'

    def get_queryset(self):
        return LectureCategory.objects.filter(is_delete=False)


class AdminGalleryCategoryCreateView(LoginRequiredMixin, CreateView):
    model = GalleryCategory
    form_class = GalleryCategoryForm
    template_name = 'userprofile_app/galleries/gallery_category_form.html'
    success_url = reverse_lazy('userprofile_app:gallery_categories_list')


class AdminGalleryCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = GalleryCategory
    form_class = GalleryCategoryForm
    template_name = 'userprofile_app/galleries/gallery_category_form.html'
    success_url = reverse_lazy('userprofile_app:gallery_categories_list')


class AdminGalleryCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = GalleryCategory
    template_name = 'userprofile_app/galleries/gallery_category_confirm_delete.html'
    success_url = reverse_lazy('userprofile_app:gallery_categories_list')


# endregion

# region Footer Link
class AdminFooterLinkListView(LoginRequiredMixin, ListView):
    model = FooterLink
    template_name = 'userprofile_app/footer_links/footer_links_list.html'


class AdminFooterLinkCreateView(LoginRequiredMixin, CreateView):
    pass


class AdminFooterLinkUpdateView(LoginRequiredMixin, UpdateView):
    model = FooterLink
    form_class = FooterLinkForm
    template_name = 'userprofile_app/footer_links/footer_link_form.html'
    success_url = reverse_lazy('userprofile_app:footer_links_list')

    def get_queryset(self):
        return GalleryImage.objects.filter(is_delete=False)


class AdminFooterLinkDeleteView(LoginRequiredMixin, DeleteView):
    model = FooterLink
    template_name = 'userprofile_app/footer_links/footer_link_confirm_delete.html'
    success_url = reverse_lazy('userprofile_app:footer_links_list')


# endregion
# region Footer Link Box
class AdminFooterLinkBoxListView(LoginRequiredMixin, ListView):
    model = GalleryCategory
    template_name = 'userprofile_app/footer_links/footer_link_boxes_list.html'


class AdminFooterLinkBoxCreateView(LoginRequiredMixin, CreateView):
    model = GalleryCategory
    form_class = GalleryCategoryForm
    template_name = 'userprofile_app/footer_links/footer_link_box_form.html'
    success_url = reverse_lazy('userprofile_app:footer_link_boxes_list')


class AdminFooterLinkBoxUpdateView(LoginRequiredMixin, UpdateView):
    model = GalleryCategory
    form_class = GalleryCategoryForm
    template_name = 'userprofile_app/footer_links/footer_link_box_form.html'
    success_url = reverse_lazy('userprofile_app:footer_link_boxes_list')


class AdminFooterLinkBoxDeleteView(LoginRequiredMixin, DeleteView):
    model = GalleryCategory
    template_name = 'userprofile_app/footer_links/footer_link_box_confirm_delete.html'
    success_url = reverse_lazy('userprofile_app:footer_link_boxes_list')


# endregion

# region Contact Us
class AdminContactUsListView(LoginRequiredMixin, ListView):
    model = ContactUs
    template_name = 'userprofile_app/contact_us/contact_us_list.html'


class AdminContactUsUpdateView(LoginRequiredMixin, UpdateView):
    model = ContactUs
    form_class = ContactUsForm
    template_name = 'userprofile_app/contact_us/contact_us_form.html'
    success_url = reverse_lazy('userprofile_app:contact_us_list')


# endregion

# region slider
class AdminSliderListView(LoginRequiredMixin, ListView):
    model = ContactUs
    template_name = 'userprofile_app/sliders/sliders_list.html'


class AdminSliderUpdateView(LoginRequiredMixin, UpdateView):
    model = Slider
    form_class = SliderForm
    template_name = 'userprofile_app/sliders/slider_form.html'
    success_url = reverse_lazy('userprofile_app:sliders_list')


# endregion

# region SiteSetting
class AdminSiteSettingListView(LoginRequiredMixin, ListView):
    model = SiteSetting
    template_name = 'userprofile_app/site_settings/site_settings_list.html'


class AdminSiteSettingUpdateView(LoginRequiredMixin, UpdateView):
    model = SiteSetting
    form_class = SiteSettingForm
    template_name = 'userprofile_app/site_settings/site_setting_form.html'
    success_url = reverse_lazy('userprofile_app:site_Settings_list')


# endregion

# region User Setting

class InformationUserProfile(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'userprofile_app/settings/information_profile_user.html'

    def get_object(self, queryset=None):
        return self.request.user


class ArticleUserPanel(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'userprofile_app/articles/articles_list.html'

    def get_queryset(self):
        return Article.objects.filter(user=self.request.user)


class EditUserProfilePage(LoginRequiredMixin, View):
    def get(self, request):
        return render(request,
                      template_name='userprofile_app/settings/edit_profile_page.html',
                      context={'user': request.user})

    def post(self, request):
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.address = request.POST.get('address', '')
        user.phone_number = request.POST.get('phone_number', '')
        user.about_user = request.POST.get('about_user')
        user.save()
        messages.success(request, 'تغییرات با موفقیت ثبت گردید')
        return redirect('userprofile_app:edit_user_profile_page')


class ChangePasswordPage(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, template_name='userprofile_app/settings/change_password_page.html')

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
