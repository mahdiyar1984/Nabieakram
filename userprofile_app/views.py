from typing import Union
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from django.db.models import QuerySet, Q, Case, When, BooleanField
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views.generic import DetailView, TemplateView
from blog_app.models import Article, ArticleCategory, ArticleTag, ArticleComment
from main_app.models import FooterLink, ContactUs, SiteSetting, Slider, FooterLinkBox
from media_app.models import Lecture, LectureCategory, LectureTag, \
    LectureComment, GalleryImage, GalleryCategory, LectureClip
from utils.email_service import send_activation_email
from .forms import ArticleForm, GroupForm, ArticleCategoryForm, ArticleTagForm, LectureForm, LectureTagForm, \
    LectureCategoryForm, GalleryImageForm, \
    GalleryCategoryForm, FooterLinkForm, ContactUsForm, SliderForm, SiteSettingForm, LectureClipForm, FooterLinkBoxForm
from django.contrib import messages
from django.http import HttpRequest, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from account_app.models import User
from .forms import UserCreateForm, UserUpdateForm
from django.contrib.auth.models import Group, Permission
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

class AuthenticatedHttpRequest(HttpRequest):
    user: Union[User, None]


# region dashboard
class UserPanelDashboardPage(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, template_name='userprofile_app/dashboard/user_panel_dashboard_page.html')


# endregion

# region user profile
class UserProfileDetailView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, template_name='userprofile_app/user_profile/user_profile_view.html')


class UserProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, template_name='userprofile_app/user_profile/user_profile_edit.html')

    def post(self, request):
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.username = request.POST.get('username', '')
        user.address = request.POST.get('address', '')
        user.phone_number = request.POST.get('phone_number', '')
        user.about_user = request.POST.get('about_user')

        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']

        user.save()
        messages.success(request, 'تغییرات با موفقیت ثبت گردید')
        return redirect('userprofile_app:user_profile_detail')


class UserProfileChangePassword(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, template_name='userprofile_app/user_profile/user_profile_change_password.html')

    def post(self, request):
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password1')
        confirm_password = request.POST.get('new_password2')

        if not old_password or not new_password or not confirm_password:
            messages.error(request, 'لطفاً همه فیلدها را پر کنید')
            return redirect('userprofile_app:user_profile_change_password')

        user = request.user
        if not user.check_password(old_password):
            messages.error(request, 'کلمه عبور وارد شده اشتباه می باشد')
            return redirect('userprofile_app:user_profile_change_password')

        if new_password != confirm_password:
            messages.error(request, 'کلمه عبور و تکرار کلمه عبور یکسان نیستند')
            return redirect('userprofile_app:user_profile_change_password')

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'کلمه عبور با موفقیت تغییر یافت')
        return redirect('userprofile_app:user_profile_change_password')


class UserProfileForgotPassword(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, template_name='userprofile_app/user_profile/user_profile_change_password.html')

    def post(self, request):
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password1')
        confirm_password = request.POST.get('new_password2')

        if not old_password or not new_password or not confirm_password:
            messages.error(request, 'لطفاً همه فیلدها را پر کنید')
            return redirect('userprofile_app:user_profile_change_password')

        user = request.user
        if not user.check_password(old_password):
            messages.error(request, 'کلمه عبور وارد شده اشتباه می باشد')
            return redirect('userprofile_app:user_profile_change_password')

        if new_password != confirm_password:
            messages.error(request, 'کلمه عبور و تکرار کلمه عبور یکسان نیستند')
            return redirect('userprofile_app:user_profile_change_password')

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'کلمه عبور با موفقیت تغییر یافت')
        return redirect('userprofile_app:user_profile_change_password')


class UserProfileChangeEmail(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, template_name='userprofile_app/user_profile/user_profile_change_email.html')

    def post(self, request):
        old_email = request.POST.get('old_email')
        new_email1 = request.POST.get('new_email1')
        new_email2 = request.POST.get('new_email2')

        if not old_email or not new_email1 or not new_email2:
            messages.error(request, 'لطفاً همه فیلدها را پر کنید')
            return redirect('userprofile_app:user_profile_change_email')

        user = User.objects.get(email=old_email)
        if not user:
            messages.error(request, 'ایمیل وارد شده اشتباه می باشد')
            return redirect('userprofile_app:user_profile_change_email')

        if new_email1 != new_email1:
            messages.error(request, 'کلمه عبور و تکرار کلمه عبور یکسان نیستند')
            return redirect('userprofile_app:user_profile_change_email')

        user.email_activation_code = get_random_string(64)
        user.pending_email = new_email1
        user.save()
        update_session_auth_hash(request, user)

        try:
            subject = "فعالسازی ایمیل شما در سایت نبی اکرم"
            text_message = "لطفا بر روی فعال شدن حساب کاربری بر روی لینک زیر کلیک بکنید."
            activation_url = reverse('userprofile_app:user_profile_activate_email', args=[user.email_activation_code])
            activation_link = request.build_absolute_uri(activation_url)

            send_activation_email(
                subject=subject,
                user=user,
                activation_link=activation_link,
                template='emails/change_email.html',
                text_message=text_message
            )

            messages.success(self.request,
                             "کد فعالسازی به ایمیل جدید شما ارسال گردید، جهت تغییر ایمیل روی لینک فعالسازی در ایمیل جدیدتان کلیک کنید.")
        except Exception as e:
            messages.warning(self.request, f"ایمیل تغییر کرد ولی کدفعالسازی به ایمیل جدید کاربر ارسال نشد ({e})")
        return redirect('userprofile_app:user_profile_change_email')


class UserProfileActiveEmailView(LoginRequiredMixin, View):
    def get(self, request, email_active_code):
        try:
            user: User = User.objects.get(email_activation_code=email_active_code)
            if user is not None:
                user.email = user.pending_email
                user.activation_code = get_random_string(64)
                user.save()
                messages.success(request, 'ایمیل شما با موفقیت تغییر یافت')

        except User.DoesNotExist:
            messages.error(request, 'کد فعالسازی معتبر نیست')

        return redirect('userprofile_app:user_profile_detail')


# endregion

# region Article

class AdminArticleListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Article
    template_name = 'userprofile_app/articles/articles_list.html'
    paginate_by = 5

    # اجازه دسترسی رو کنترل می‌کنه
    def test_func(self):
        return (
                self.request.user.is_superuser or
                self.request.user.groups.filter(name__in=['editor', 'manager', 'author']).exists()
        )

    # اگر دسترسی نداشت خطا میده
    def handle_no_permission(self):
        return HttpResponseForbidden('شما اجازه دسترسی به این صفحه را ندارید.')

    # کوئری را کنترل می کند
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name__in=['editor','manager']).exists():
            queryset = Article.objects.all().order_by('-create_date')
        else:
            queryset = Article.objects.filter(
                Q(status='published') | Q(author=user)
            ).annotate(  # وقتی لیست مقالات رو نشون می‌دی: مقاله‌هایی که خود کاربر نوشته بیاد بالاتر، بعدش مقاله‌های بقیه که منتشر شدن.
                is_owner=Case(
                    When(author=user, then=True),
                    default=False,
                    output_field=BooleanField()
                )
            ).order_by('-is_owner', '-create_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # 🔹 نقش کاربر را در قالب بفرست
        context['is_author'] = user.groups.filter(name='author').exists()
        context['is_editor_or_manager'] = (
                user.is_superuser or user.groups.filter(name__in=['editor', 'manager']).exists()
        )

        return context
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
class AdminArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'userprofile_app/articles/article_form.html'
    success_url = reverse_lazy('userprofile_app:articles_list')

    def test_func(self):
        user = self.request.user
        article = get_object_or_404(Article, pk=self.kwargs['pk'])

        # اگر سوپریوزر یا منیجر یا ادیتور باشد، اجازه ویرایش دارد
        if user.is_superuser or user.groups.filter(name__in=['manager', 'editor']).exists():
            return True

        # اگر نویسنده باشد فقط مقاله خودش را بتواند ویرایش کند
        if user.groups.filter(name='author').exists() and article.author == user:
            return True

        # در غیر این صورت اجازه ندارد
        return False

    def handle_no_permission(self):
        return HttpResponseForbidden('شما اجازه ویرایش این مقاله را ندارید.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ArticleCategory.objects.all()
        context['tags'] = ArticleTag.objects.all()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)

        # اگر نویسنده مقاله را تغییر دهد، نویسنده فعلی همان کاربر باقی می‌ماند
        if not self.request.user.is_superuser and not self.request.user.groups.filter(name__in=['manager', 'editor']).exists():
            self.object.author = self.request.user

        # اگر تصویر جدید آپلود شده باشد
        if self.request.FILES.get('image'):
            self.object.image = self.request.FILES['image']

        # وضعیت مقاله (در صورت نیاز)
        if self.object.status in ['rejected', 'draft', 'pending']:
            self.object.status = 'draft'
        self.object.status = 'draft'
        self.object.save()

        # ذخیره ManyToMany
        self.object.selected_categories.set(form.cleaned_data['selected_categories'])
        self.object.selected_tags.set(form.cleaned_data['selected_tags'])

        return super().form_valid(form)
class AdminArticleDeleteView(LoginRequiredMixin, View):
    success_url = reverse_lazy('userprofile_app:articles_list')

    def post(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        user = request.user

        # فقط superuser، manager و editor مجازند
        if user.is_superuser or user.groups.filter(name__in=['manager', 'editor']).exists():
            article.is_delete = True
            article.save()
            messages.success(request, "مقاله با موفقیت حذف شد.")
        else:
            messages.error(request, "شما اجازه حذف مقاله را ندارید.")

        return redirect(self.success_url)
class AdminArticleChangeStatusView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        action = request.POST.get("action")

        # if author wants to do pending in himself article
        if action == "submit_for_review":
            if article.status == "draft" and (
                    request.user == article.author
                    or request.user.is_superuser
                    or request.user.groups.filter(name__in=["manager", "editor"]).exists()
            ):
                article.status = "pending"
                article.save()
                messages.success(request, "مقاله برای بررسی ارسال شد.")
            else:
                messages.error(request, "شما مجاز به ارسال این مقاله نیستید.")

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


@login_required
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


@login_required
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


@login_required
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


@login_required
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

@login_required
def admin_article_comment_list(request: HttpRequest):
    article_comments: QuerySet[ArticleComment] = (
        ArticleComment.objects
        .select_related('article', 'user')
        .prefetch_related('articlecomment_set__user')
        .filter(parent__isnull=True)
        .order_by('-create_date')
    )
    paginator = Paginator(article_comments, 5)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    context = {
        'page_obj': page_obj
    }
    return render(request, template_name='userprofile_app/articles/article_comments_list.html', context=context)


@login_required
def admin_article_comment_read(request: HttpRequest, pk):
    comment: ArticleComment = ArticleComment.objects.get(pk=pk)
    context = {
        'comment': comment,
        'read_only': True
    }
    return render(request, 'userprofile_app/articles/article_comment_form.html', context)


@login_required
def admin_article_comment_update(request: AuthenticatedHttpRequest, pk):
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


@login_required
def admin_article_comment_delete(request: HttpRequest, pk):
    comment: ArticleComment = ArticleComment.objects.get(pk=pk)
    comment.is_delete = True
    comment.save()
    return redirect('userprofile_app:article_comments_list')


# endregion

# region Lecture

class AdminLectureListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Lecture
    template_name = 'userprofile_app/lectures/lectures_list.html'
    paginate_by = 5

    # اجازه دسترسی رو کنترل می‌کنه
    def test_func(self):
        return (
                self.request.user.is_superuser or
                self.request.user.groups.filter(name__in=['editor', 'manager', 'author']).exists()
        )

    # اگر دسترسی نداشت خطا میده
    def handle_no_permission(self):
        return HttpResponseForbidden('شما اجازه دسترسی به این صفحه را ندارید.')

    # کوئری را کنترل می کند
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name__in=['editor', 'manager']).exists():
            queryset = Article.objects.all().order_by('-create_date')
        else:
            queryset = Lecture.objects.filter(
                Q(status='published') | Q(author=user)
            ).annotate(  # وقتی لیست مقالات رو نشون می‌دی: مقاله‌هایی که خود کاربر نوشته بیاد بالاتر، بعدش مقاله‌های بقیه که منتشر شدن.
                is_owner=Case(
                    When(author=user, then=True),
                    default=False,
                    output_field=BooleanField()
                )
            ).order_by('-is_owner', '-created_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # 🔹 نقش کاربر را در قالب بفرست
        context['is_author'] = user.groups.filter(name='author').exists()
        context['is_editor_or_manager'] = (
                user.is_superuser or user.groups.filter(name__in=['editor', 'manager']).exists()
        )

        return context
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

        if self.request.FILES.get('image'):
            self.object.image = self.request.FILES['image']

        if self.request.FILES.get('video'):
            self.object.video = self.request.FILES['video']

        if self.request.FILES.get('audio'):
            self.object.audio = self.request.FILES['audio']

        if self.object.status in ['rejected', 'draft', 'pending']:
            self.object.status = 'draft'

        self.object.save()
        form.save_m2m()
        return redirect(self.get_success_url())
class AdminLectureUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Lecture
    form_class = LectureForm
    template_name = 'userprofile_app/lectures/lecture_form.html'
    success_url = reverse_lazy('userprofile_app:lectures_list')

    def test_func(self):
        lecture = self.get_object()
        user = self.request.user

        # فقط مدیر، سوپریوزر یا ادیتور می‌تونن هر درسی رو ویرایش کنن
        if user.is_superuser or user.groups.filter(name__in=['manager', 'editor']).exists():
            return True

        # نویسنده فقط درس خودش رو می‌تونه ویرایش کنه
        if user.groups.filter(name='author').exists() and lecture.author == user:
            return True

        return False

    def handle_no_permission(self):
        return HttpResponseForbidden('شما اجازه ویرایش این درس را ندارید.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = LectureCategory.objects.all()
        context['tags'] = LectureTag.objects.all()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)

        if not self.request.user.is_superuser and not self.request.user.groups.filter(name__in=['manager', 'editor']).exists():
            self.object.author = self.request.user

        if self.request.FILES.get('image'):
            self.object.image = self.request.FILES['image']

        if self.request.FILES.get('video'):
            self.object.video = self.request.FILES['video']

        if self.request.FILES.get('audio'):
            self.object.audio = self.request.FILES['audio']

        if self.object.status in ['rejected', 'draft', 'pending']:
            self.object.status = 'draft'

        self.object.status = 'draft'

        self.object.save()

        # ذخیره ManyToMany
        self.object.selected_categories.set(form.cleaned_data['selected_categories'])
        self.object.selected_tags.set(form.cleaned_data['selected_tags'])

        return super().form_valid(form)
class AdminLectureDeleteView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('userprofile_app:lectures_list')

    def post(self, request, pk, *args, **kwargs):
        lecture = get_object_or_404(Lecture, pk=pk)
        user = request.user

        # فقط superuser، manager و editor مجازند
        if user.is_superuser or user.groups.filter(name__in=['manager', 'editor']).exists():
            lecture.is_delete = True
            lecture.save()
            messages.success(request, "مقاله با موفقیت حذف شد.")
        else:
            messages.error(request, "شما اجازه حذف مقاله را ندارید.")
class AdminLectureChangeStatusView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        lecture = get_object_or_404(Lecture, pk=pk)
        action = request.POST.get("action")

        # if lecture wants to do pending in himself lecture
        if action == "submit_for_review":
            if lecture.status == "draft" and (
                    request.user == lecture.author
                    or request.user.is_superuser
                    or request.user.groups.filter(name__in=["manager", "editor"]).exists()
            ):
                lecture.status = "pending"
                lecture.save()
                messages.success(request, "سخنرانی برای بررسی ارسال شد.")
            else:
                messages.error(request, "شما مجاز به ارسال این سخنرانی نیستید.")

        # if editor or admin wants to confirm the lecture
        if action == "publish" and request.user.has_perm("media_app.publish_lecture"):
            lecture.status = "published"
            lecture.save()
            messages.success(request, "سخنرانی منتشر شد.")
            return redirect("userprofile_app:lectures_list")

        # if editor or admin wants to reject the lecture
        if action == "reject" and request.user.has_perm("media_app.reject_lecture"):
            lecture.status = "rejected"
            lecture.save()
            messages.warning(request, "سخنرانی رد شد.")
            return redirect("userprofile_app:lectures_list")

        messages.error(request, "شما اجازه این کار را ندارید.")
        return redirect("userprofile_app:lectures_list")

# endregion
# region Lecture Category
class AdminLectureCategoryListView(LoginRequiredMixin, ListView):
    model = LectureCategory
    template_name = 'userprofile_app/lectures/lecture_categories_list.html'
    paginate_by = 10


class AdminLectureCategoryReadView(LoginRequiredMixin, DetailView):
    model = LectureCategory
    form_class = LectureCategoryForm
    template_name = "userprofile_app/lectures/lecture_category_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LectureCategoryForm(instance=self.get_object(), read_only=True)
        context['read_only'] = getattr(context.get('form'), 'read_only', True)
        return context


class AdminLectureCategoryCreateView(LoginRequiredMixin, CreateView):
    model = LectureCategory
    form_class = LectureCategoryForm
    template_name = 'userprofile_app/lectures/lecture_category_form.html'
    success_url = reverse_lazy('userprofile_app:lecture_categories_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)


class AdminLectureCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = LectureCategory
    form_class = LectureCategoryForm
    template_name = 'userprofile_app/lectures/lecture_category_form.html'
    success_url = reverse_lazy('userprofile_app:lecture_categories_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)


class AdminLectureCategoryDeleteView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('userprofile_app:lecture_categories_list')

    def post(self, request, pk, *args, **kwargs):
        lecture_category = get_object_or_404(LectureCategory, pk=pk)
        lecture_category.is_delete = True
        lecture_category.save()
        return redirect(self.success_url)


# endregion
# region Lecture Tag
class AdminLectureTagListView(LoginRequiredMixin, ListView):
    model = LectureTag
    template_name = 'userprofile_app/lectures/lecture_tags_list.html'
    paginate_by = 10


class AdminLectureTagReadView(LoginRequiredMixin, DetailView):
    model = LectureTag
    form_class = LectureTagForm
    template_name = "userprofile_app/lectures/lecture_tag_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LectureTagForm(instance=self.get_object(), read_only=True)
        context['read_only'] = getattr(context.get('form'), 'read_only', True)
        return context


class AdminLectureTagCreateView(LoginRequiredMixin, CreateView):
    model = LectureTag
    form_class = LectureTagForm
    template_name = 'userprofile_app/lectures/lecture_tag_form.html'
    success_url = reverse_lazy('userprofile_app:lecture_tags_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)


class AdminLectureTagUpdateView(LoginRequiredMixin, UpdateView):
    model = LectureTag
    form_class = LectureTagForm
    template_name = 'userprofile_app/lectures/lecture_tag_form.html'
    success_url = reverse_lazy('userprofile_app:lecture_tags_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)


class AdminLectureTagDeleteView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('userprofile_app:lecture_tags_list')

    def post(self, request, pk, *args, **kwargs):
        lecture_tag = get_object_or_404(LectureTag, pk=pk)
        lecture_tag.is_delete = True
        lecture_tag.save()
        return redirect(self.success_url)


# endregion
# region Lecutre Comment

@login_required
def admin_lecture_comment_list(request: HttpRequest):
    lecture_comments: QuerySet[LectureComment] = (
        LectureComment.objects
        .select_related('lecture', 'user')
        .prefetch_related('lecturecomment_set__user')
        .filter(parent__isnull=True)
        .order_by('-created_date')
    )
    paginator = Paginator(lecture_comments, 5)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    context = {
        'page_obj': page_obj
    }
    return render(request, template_name='userprofile_app/lectures/lecture_comments_list.html', context=context)


@login_required
def admin_lecture_comment_read(request: HttpRequest, pk):
    comment: LectureComment = LectureComment.objects.get(pk=pk)
    context = {
        'comment': comment,
        'read_only': True
    }
    return render(request, 'userprofile_app/lectures/lecture_comment_form.html', context)


@login_required
def admin_lecture_comment_update(request: AuthenticatedHttpRequest, pk):
    comment: LectureComment = LectureComment.objects.get(pk=pk)
    if request.method == 'POST':
        comment.text = request.POST.get('text', comment.text)
        comment.is_active = 'is_active' in request.POST
        comment.is_delete = 'is_delete' in request.POST
        comment.save()

        if comment.parent:
            comment.parent.is_active = 'is_active_parent' in request.POST
            comment.parent.is_delete = 'is_delete_parent' in request.POST
            comment.parent.save()

        reply_text = request.POST.get('reply_text')
        if reply_text:
            first_reply = comment.lecturecomment_set.first()
            if first_reply:
                first_reply.text = reply_text
                first_reply.save()
            else:
                LectureComment.objects.create(
                    lecture=comment.lecture,
                    user=request.user,
                    parent=comment,
                    text=reply_text
                )

        return redirect('userprofile_app:lecture_comments_list')

    context = {'comment': comment, 'read_only': False}
    return render(request, 'userprofile_app/lectures/lecture_comment_form.html', context)


@login_required
def admin_lecture_comment_delete(request: HttpRequest, pk):
    comment: LectureComment = LectureComment.objects.get(pk=pk)
    comment.is_delete = True
    comment.save()
    return redirect('userprofile_app:lecture_comments_list')


# endregion
# region Lecture Clip
class AdminLectureClipListView(LoginRequiredMixin, ListView):
    model = LectureClip
    template_name = 'userprofile_app/lectures/lecture_clips_list.html'
    paginate_by = 5


class AdminLectureClipReadView(LoginRequiredMixin, DetailView):
    model = LectureClip
    form_class = LectureClipForm
    template_name = "userprofile_app/lectures/lecture_clip_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LectureClipForm(instance=self.get_object(), read_only=True)
        context['read_only'] = getattr(context.get('form'), 'read_only', True)
        return context


class AdminLectureClipCreateView(LoginRequiredMixin, CreateView):
    model = LectureClip
    form_class = LectureClipForm
    template_name = 'userprofile_app/lectures/lecture_clip_form.html'
    success_url = reverse_lazy('userprofile_app:lecture_clips_list')

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.get_success_url())


class AdminLectureClipUpdateView(LoginRequiredMixin, UpdateView):
    model = LectureClip
    form_class = LectureClipForm
    template_name = 'userprofile_app/lectures/lecture_clip_form.html'
    success_url = reverse_lazy('userprofile_app:lecture_clips_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.request.FILES.get('video'):
            self.object.video = self.request.FILES['video']
        self.object.save()
        return super().form_valid(form)


class AdminLectureClipDeleteView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('userprofile_app:lecture_clips_list')

    def post(self, request, pk, *args, **kwargs):
        lecture_clip = get_object_or_404(LectureClip, pk=pk)
        lecture_clip.is_delete = True
        lecture_clip.save()
        return redirect(self.success_url)


# endregion

# region Gallery
class AdminGalleryImageListView(LoginRequiredMixin, ListView):
    model = GalleryImage
    template_name = 'userprofile_app/galleries/galleries_list.html'
    paginate_by = 5


class AdminGalleryImageReadView(LoginRequiredMixin, DetailView):
    model = GalleryImage
    form_class = GalleryImageForm
    template_name = "userprofile_app/galleries/gallery_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = GalleryImageForm(instance=self.get_object(), read_only=True)
        context['read_only'] = getattr(context.get('form'), 'read_only', True)
        return context


class AdminGalleryImageCreateView(LoginRequiredMixin, CreateView):
    model = GalleryImage
    form_class = GalleryImageForm
    template_name = 'userprofile_app/galleries/gallery_form.html'
    success_url = reverse_lazy('userprofile_app:galleries_list')

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.get_success_url())


class AdminGalleryImageUpdateView(LoginRequiredMixin, UpdateView):
    model = GalleryImage
    form_class = GalleryImageForm
    template_name = 'userprofile_app/galleries/gallery_form.html'
    success_url = reverse_lazy('userprofile_app:galleries_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.request.FILES.get('image'):
            self.object.image = self.request.FILES['image']
        return super().form_valid(form)


class AdminGalleryImageDeleteView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('userprofile_app:galleries_list')

    def post(self, request, pk, *args, **kwargs):
        lecture = get_object_or_404(GalleryImage, pk=pk)
        lecture.is_delete = True
        lecture.save()
        return redirect(self.success_url)


# endregion
# region Gallery Category
class AdminGalleryCategoryListView(LoginRequiredMixin, ListView):
    model = GalleryCategory
    template_name = 'userprofile_app/galleries/gallery_categories_list.html'
    paginate_by = 10


class AdminGalleryCategoryReadView(LoginRequiredMixin, DetailView):
    model = GalleryCategory
    form_class = GalleryCategoryForm
    template_name = "userprofile_app/galleries/gallery_category_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = GalleryCategoryForm(instance=self.get_object(), read_only=True)
        context['read_only'] = getattr(context.get('form'), 'read_only', True)
        return context


class AdminGalleryCategoryCreateView(LoginRequiredMixin, CreateView):
    model = GalleryCategory
    form_class = GalleryCategoryForm
    template_name = 'userprofile_app/galleries/gallery_category_form.html'
    success_url = reverse_lazy('userprofile_app:gallery_categories_list')

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class AdminGalleryCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = GalleryCategory
    form_class = GalleryCategoryForm
    template_name = 'userprofile_app/galleries/gallery_category_form.html'
    success_url = reverse_lazy('userprofile_app:gallery_categories_list')

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class AdminGalleryCategoryDeleteView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('userprofile_app:gallery_categories_list')

    def post(self, request, pk, *args, **kwargs):
        gallery_category = get_object_or_404(GalleryCategory, pk=pk)
        gallery_category.is_delete = True
        gallery_category.save()
        return redirect(self.success_url)


# endregion

# region Footer Link
class AdminFooterLinkListView(LoginRequiredMixin, ListView):
    model = FooterLink
    template_name = 'userprofile_app/footer_links/footer_links_list.html'
    paginate_by = 5


class AdminFooterLinkReadView(LoginRequiredMixin, DetailView):
    model = FooterLink
    form_class = LectureForm
    template_name = "userprofile_app/footer_links/footer_link_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FooterLinkForm(instance=self.get_object(), read_only=True)
        context['read_only'] = getattr(context.get('form'), 'read_only', True)
        context['footer_link_box'] = FooterLinkBox.objects.all()
        return context


class AdminFooterLinkCreateView(LoginRequiredMixin, CreateView):
    model = FooterLink
    form_class = FooterLinkForm
    template_name = 'userprofile_app/footer_links/footer_link_form.html'
    success_url = reverse_lazy('userprofile_app:footer_links_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect(self.get_success_url())


class AdminFooterLinkUpdateView(LoginRequiredMixin, UpdateView):
    model = FooterLink
    form_class = FooterLinkForm
    template_name = 'userprofile_app/footer_links/footer_link_form.html'
    success_url = reverse_lazy('userprofile_app:footer_links_list')

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class AdminFooterLinkDeleteView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('userprofile_app:footer_links_list')

    def post(self, request, pk, *args, **kwargs):
        footer_link = get_object_or_404(FooterLink, pk=pk)
        footer_link.is_active = False
        footer_link.save()
        return redirect(self.success_url)


# endregion
# region Footer Link Box
class AdminFooterLinkBoxListView(LoginRequiredMixin, ListView):
    model = FooterLinkBox
    template_name = 'userprofile_app/footer_links/footer_link_boxes_list.html'
    paginate_by = 5


class AdminFooterLinkBoxReadView(LoginRequiredMixin, DetailView):
    model = FooterLinkBox
    form_class = FooterLinkBoxForm
    template_name = "userprofile_app/footer_links/footer_link_box_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LectureCategoryForm(instance=self.get_object(), read_only=True)
        context['read_only'] = getattr(context.get('form'), 'read_only', True)
        return context


class AdminFooterLinkBoxCreateView(LoginRequiredMixin, CreateView):
    model = FooterLinkBox
    form_class = FooterLinkBoxForm
    template_name = 'userprofile_app/footer_links/footer_link_box_form.html'
    success_url = reverse_lazy('userprofile_app:footer_link_boxes_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)


class AdminFooterLinkBoxUpdateView(LoginRequiredMixin, UpdateView):
    model = FooterLinkBox
    form_class = FooterLinkBoxForm
    template_name = 'userprofile_app/footer_links/footer_link_box_form.html'
    success_url = reverse_lazy('userprofile_app:footer_link_boxes_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)


class AdminFooterLinkBoxDeleteView(DeleteView):
    success_url = reverse_lazy('userprofile_app:footer_link_boxes_list')

    def post(self, request, pk, *args, **kwargs):
        footer_link_box = get_object_or_404(FooterLinkBox, pk=pk)
        footer_link_box.is_active = False
        footer_link_box.save()
        return redirect(self.success_url)


# endregion

# region Contact Us
class AdminContactUsListView(LoginRequiredMixin, ListView):
    model = ContactUs
    template_name = 'userprofile_app/contact_us/contact_us_list.html'
    paginate_by = 10


class AdminContactUsReadView(LoginRequiredMixin, DetailView):
    model = ContactUs
    form_class = ContactUsForm
    template_name = "userprofile_app/contact_us/contact_us_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactUsForm(instance=self.get_object(), read_only=True)
        context['read_only'] = getattr(context.get('form'), 'read_only', True)
        return context


class AdminContactUsUpdateView(LoginRequiredMixin, UpdateView):
    model = ContactUs
    form_class = ContactUsForm
    template_name = 'userprofile_app/contact_us/contact_us_form.html'
    success_url = reverse_lazy('userprofile_app:contact_us_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.is_replied = True
        self.object.response_date = timezone.now()
        self.object.save()
        # ارسال ایمیل به کاربر
        try:
            subject = "پاسخ به پیام شما در سایت"
            text_message = self.object.response or "پاسخ شما از طرف پشتیبانی سایت ارسال شد."
            activation_link = None  # اینجا لینک خاصی لازم نیست ولی تابع شما نیازش داره

            send_activation_email(
                subject=subject,
                user=self.object.author,
                activation_link=activation_link,
                template='emails/contact_response.html',
                text_message=text_message
            )

            messages.success(self.request, "پاسخ با موفقیت ذخیره و به ایمیل کاربر ارسال شد.")
        except Exception as e:
            messages.warning(self.request, f"پاسخ ذخیره شد ولی ایمیل ارسال نشد ({e})")
        return super().form_valid(form)


# endregion

# region Slider
class AdminSliderListView(LoginRequiredMixin, ListView):
    model = Slider
    template_name = 'userprofile_app/sliders/sliders_list.html'
    paginate_by = 5


class AdminSliderReadView(LoginRequiredMixin, DetailView):
    model = Slider
    form_class = SliderForm
    template_name = "userprofile_app/sliders/slider_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SliderForm(instance=self.get_object(), read_only=True)
        context['read_only'] = getattr(context.get('form'), 'read_only', True)
        return context


class AdminSliderCreateView(LoginRequiredMixin, CreateView):
    model = Slider
    form_class = SliderForm
    template_name = 'userprofile_app/sliders/slider_form.html'
    success_url = reverse_lazy('userprofile_app:sliders_list')

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.get_success_url())


class AdminSliderUpdateView(LoginRequiredMixin, UpdateView):
    model = Slider
    form_class = SliderForm
    template_name = 'userprofile_app/sliders/slider_form.html'
    success_url = reverse_lazy('userprofile_app:sliders_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.request.FILES.get('image'):
            self.object.image = self.request.FILES['image']
        return super().form_valid(form)


class AdminSliderDeleteView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('userprofile_app:sliders_list')

    def post(self, request, pk, *args, **kwargs):
        slider = get_object_or_404(Slider, pk=pk)
        slider.is_active = False
        slider.save()
        return redirect(self.success_url)


# endregion

# region SiteSetting
class AdminSiteSettingUpdateView(LoginRequiredMixin, UpdateView):
    model = SiteSetting
    form_class = SiteSettingForm
    template_name = 'userprofile_app/site_settings/site_setting_form.html'

    def get_success_url(self):
        # بعد از ذخیره، دوباره به همان صفحه ویرایش بازگردد
        return reverse_lazy(
            'userprofile_app:site_setting_edit',
            kwargs={'pk': self.object.pk}
        )

    def form_valid(self, form):
        # ذخیره لوگو اگر آپلود شده باشد
        if self.request.FILES.get('logo'):
            form.instance.site_logo = self.request.FILES['logo']
        response = super().form_valid(form)
        # پیام موفقیت
        messages.success(self.request, "تنظیمات سایت با موفقیت ذخیره شد!")
        return response
# endregion

# region Groups
class GroupPermissionMatrixView(LoginRequiredMixin, TemplateView):
    template_name = "userprofile_app/groups/groups_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        groups = Group.objects.all()
        actions = ["add", "change", "delete", "view", "publish", "reject"]

        # ✳️ تعیین مجوزهای قابل نمایش
        if self.request.user.is_superuser:
            # superuser همه مجوزها را ببیند
            permissions = Permission.objects.all().select_related("content_type")
        else:
            # فقط مجوزهایی که در DashboardPermissionView تعریف شده‌اند
            permissions = Permission.objects.filter(
                dashboardpermissionview__isnull=False
            ).select_related("content_type").distinct()

        # ⚙️ ساخت دیکشنری اپلیکیشن‌ها و مدل‌ها
        apps_dict = {}
        for perm in permissions:
            app_label = perm.content_type.app_label
            model_name = perm.content_type.model  # lowercase
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

        # افزودن مجوزهای هر گروه برای تیک خوردن چک‌باکس‌ها
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
        perm_map = {p.codename: p for p in all_perms}

        for group in groups:
            selected_codenames = request.POST.getlist(f'permissions_{group.id}[]')
            selected_perms = [perm_map[c] for c in selected_codenames if c in perm_map]
            group.permissions.set(selected_perms)

        return redirect(request.path)


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = "userprofile_app/groups/group_form.html"
    success_url = reverse_lazy("group_list")


class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = "userprofile_app/groups/group_form.html"
    success_url = reverse_lazy("group_list")


class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = "userprofile_app/groups/group_confirm_delete.html"
    success_url = reverse_lazy("group_list")


# endregion

# region user
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "userprofile_app/users/user_list.html"
    paginate_by = 5


class UserCreateView(LoginRequiredMixin, CreateView):
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


class UserUpdateView(LoginRequiredMixin, UpdateView):
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


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "userprofile_app/users/user_confirm_delete.html"
    success_url = reverse_lazy('userprofile_app:user_list')

# endregion
