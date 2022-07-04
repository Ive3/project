from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.signing import BadSignature
from django.contrib import messages
# Create your views here.
from .utilities import signer, send_activation_notification
from .models import RegistrationUser
from .forms import RegistrationUserForm, MyRegisterUserForm, LoginForm, ChangePassForm, ChangeUserInfoForm


# Registration user ------------------------------------------------------------
def registration(request):
    if request.method == "POST":
        form = RegistrationUserForm(request.POST)
        myform = MyRegisterUserForm(request.POST)
        if form.is_valid() and myform.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            send_activation_notification(user)
            myuser = myform.save(commit=False)
            myuser.user = user
            myuser.save()
            return redirect('registration:registration_done')
    else:
        form = RegistrationUserForm()
        myform = MyRegisterUserForm()
    context = {'form': form, 'myform': myform}
    return render(request, 'registration/registration_user.html', context)


# Registration done ------------------------------------------------------------
class RegistrationDoneView(TemplateView):
    template_name = 'registration/registration_done.html'
    title = 'Registration done'


# Activete user ------------------------------------------------------------
def user_activeted(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'registration/bad_signeture.html')
    user = get_object_or_404(User, username=username)
    if user.is_active:
        template = 'registration/user_is_activated.html'
    else:
        template = 'registration/activation_done.html'
        user.is_active = True
        user.save()
    return render(request, template)


# Login user ------------------------------------------------------------
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('mainapp:index')
    else:
        form = LoginForm
    context = {'form': form}
    return render(request, 'registration/login_user.html', context)


# Logout user ------------------------------------------------------------
@login_required()
def logout_user(request):
    logout(request)
    return redirect('registration:logout_view')


# Logout view user ------------------------------------------------------------
def logout_view(reqeust):
    return render(reqeust, 'registration/logout_user.html')


# Change password --------------------------------------------------------------
@login_required()
def change_password(request):
    if request.method == 'POST':
        form = ChangePassForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request=request, user=form.user)
            return redirect('registration:change_password_done')
    else:
        form = ChangePassForm(user=request.user)
    context = {'form': form}
    return render(request, 'registration/change_pass_user.html', context)


# Change password done --------------------------------------------------------------
class ChangePasswordDone(LoginRequiredMixin, TemplateView):
    template_name = 'registration/change_password_done.html'


# Reset Password --------------------------------------------------------------
class ResetPassView(PasswordResetView):
    template_name = 'registration/reset_pass_user.html'
    subject_template_name = 'registration/reset_subject.txt'
    email_template_name = 'registration/reset_email.txt'
    from_email = 'test1tmps1@gmail.com'
    success_url = reverse_lazy('registration:reset_password_done')


class ResetPassViewDone(PasswordResetDoneView):
    template_name = 'registration/reset_pass_done.html'


class ResetPassViewConfirm(PasswordResetConfirmView):
    template_name = 'registration/reset_pass_confirm.html'
    post_reset_login = True
    success_url = reverse_lazy('registration:reset_password_complete')


class ResetPassViewComplete(PasswordResetCompleteView):
    template_name = 'registration/reset_pass_complete.html'


# User profile page ------------------------------------------------------------
@login_required()
def ProfileView(request, pk):
    profile = RegistrationUser.objects.get(user=request.user.pk)
    context = {'profile': profile}
    return render(request, 'registration/profile.html', context)


# Update profile page ------------------------------------------------------------
@login_required()
def UpdateProfile(request, pk):
    extra_info = RegistrationUser.objects.get(user=request.user.pk)
    user = User.objects.get(pk=request.user.pk)
    if request.method == "POST":
        myform = MyRegisterUserForm(request.POST, instance=extra_info)
        form = ChangeUserInfoForm(request.POST, instance=user)
        if form.is_valid() and myform.is_valid():
            u = form.save()
            myuser = myform.save(commit=False)
            myuser.user = u
            myuser.save()
            messages.success(request, 'Your info has changed')
            return HttpResponseRedirect(reverse('registration:profile', kwargs={'pk': request.user.pk}))
    else:
        myform = MyRegisterUserForm(instance=extra_info)
        form = ChangeUserInfoForm(instance=user)
    context = {'myform': myform, 'form':form}
    return render(request, 'registration/change_user_info.html', context)


# Delete user ------------------------------------------------------------
class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'registration/delete_user.html'
    success_url = reverse_lazy('registration:delete_user_done')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class DeleteUserDone(TemplateView):
    template_name = 'registration/delete_user_done.html'
    