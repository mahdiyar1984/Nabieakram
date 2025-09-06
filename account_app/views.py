from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View

from account_app.models import User


class RegisterView(View):
    def get(self, request):
        return render(request, 'account_app/register.html')

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password1")
        confirm_password = request.POST.get("password2")

        if not email or not password or not confirm_password:
            messages.error(request, "لطفا همه فیلدها را پر کنید")
            return redirect('account_app:register_page')

        if password != confirm_password:
            messages.error(request, "کلمه‌های عبور مطابقت ندارند")
            return redirect('account_app:register_page')

        if User.objects.filter(email=email).exists():
            messages.error(request, "این ایمیل قبلا ثبت شده است")
            return redirect('account_app:register_page')

        username = email.split("@")[0]
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f'{username}{counter}'
            counter += 1

        activation_code = get_random_string(64)

        new_user = User(
            username=username,
            email=email,
            email_activation_code=activation_code,
            is_active=False,
        )
        new_user.set_password(password)
        new_user.save()

    #     activation_url = reverse('activate_account_page', args=[new_user.email_activation_code])
    #     activation_link = request.build_absolute_uri(activation_url)
    #
    #     send_activation_email('فعالسازی حساب کاربری',
    #                           new_user,
    #                           activation_link,
    #                           'emails/email_service.html',
    #                           'کاربر گرامی، جهت فعالسازی حساب کاربری روی لینک زیر کلیک کنید')
    #
        messages.success(request, "ثبت‌ نام با موفقیت انجام شد. حالا می‌تونید وارد بشید.")
        return redirect('account_app:login_page')


class ActiveAccountView(View):
    def get(self, request, email_active_code):
        try:
            user: User = User.objects.get(email_activation_code=email_active_code)
            if user is not None:
                if user.is_active:
                    messages.error(request, 'حساب کاربری فعال می باشد')
                else:
                    user.is_active = True
                    user.activation_code = get_random_string(64)
                    user.save()
                    messages.success(request, 'حساب کاربری شما با موفقیت فعال شد')
        except User.DoesNotExist:
            messages.error(request, 'کد فعالسازی معتبر نیست')

        return redirect('account_app:login_page')


class LoginView(View):
    def get(self, request):
        return render(request, template_name='account_app/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'لطفاً همه فیلدها را پر کنید')
            return redirect('account_app:login_page')

        user = User.objects.get(email=email)
        if user is not None:
            if not user.is_active:
                messages.error(request, 'حساب کاربری شما فعال نشده است')
                return redirect('account_app:login_page')
            else:
                is_password_match: bool = user.check_password(password)
                if is_password_match:
                    login(request, user)
                    return redirect('main_app:index')
                else:
                    messages.error(request, 'کلمه عبور اشتباه است')
        else:
            messages.error(request, 'کاربری با مشخصات وارد شده یافت نشد')
            return redirect('account_app:login_page')



class ForgotPasswordView(View):
    def get(self, request):
        return render(request, template_name='account_app/forgot_password.html')

    def post(self, request):
        email = request.POST.get('email')
        if email is None:
            messages.error(request, 'لطفا فیلد را پر کنید')

        user: User = User.objects.filter(email=email).first()
        if user is None:
            messages.error(request, 'اگر ایمیل شما در سایت ثبت شده باشد، لینک بازیابی ارسال خواهد شد')
        else:
            pass
            # activation_url = reverse('reset_password_page', args=[user.email_activation_code])
            # activation_link = request.build_absolute_uri(activation_url)
            #
            # send_activation_email('بازیابی  کلمه عبور',
            #                       user,
            #                       activation_link,
            #                       'emails/email_service.html',
            #                       'کاربر گرامی، جهت بازیابی کلمه عبور روی لینک زیر کلیک کنید')

            messages.success(request, 'لطفاً ایمیل خود را برای بازیابی کلمه عبور بررسی کنید.')
            return redirect('account_app:login_page')


class ResetPasswordView(View):
    def get(self, request: HttpRequest, email_active_code):
        user: User = User.objects.get(email_activation_code=email_active_code)
        if user is None:
            return redirect('account_app:login_page')
        return render(request, template_name='account_app/reset_password.html')

    def post(self, request: HttpRequest, email_active_code):
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        user: User = User.objects.filter(email_activation_code=email_active_code).first()
        if user is None:
            return redirect('account_app:login_page')
        else:
            if password != confirm_password:
                messages.error(request, 'کلمه عبور با تکرار کلمه عبور تطبیق ندارند')
                return redirect('reset_password_page', email_active_code=email_active_code)
            user.set_password(password)
            user.email_activation_code = get_random_string(64)
            user.is_active = True
            user.save()
            messages.success(request, 'کلمه عبور با موفقیت تغییر یافت می توانید در سایت وارد شوید')
            return redirect('account_app:login_page')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('account_app:login_page')
