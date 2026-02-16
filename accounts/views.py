from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView, TemplateView
from django.contrib.auth.views import (
    PasswordChangeView as DjangoPasswordChangeView,
    PasswordChangeDoneView as DjangoPasswordChangeDoneView,
    PasswordResetView as DjangoPasswordResetView,
    PasswordResetDoneView as DjangoPasswordResetDoneView,
    PasswordResetConfirmView as DjangoPasswordResetConfirmView,
    PasswordResetCompleteView as DjangoPasswordResetCompleteView,
)
from .forms import ProfileUpdateForm

User = get_user_model()


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'user_obj'

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


class PasswordChangeView(LoginRequiredMixin, DjangoPasswordChangeView):
    template_name = 'accounts/password_change_form.html'
    success_url = reverse_lazy('password_change_done')


class PasswordChangeDoneView(LoginRequiredMixin, DjangoPasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'


class PasswordResetView(DjangoPasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')


class PasswordResetDoneView(DjangoPasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(DjangoPasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class PasswordResetCompleteView(DjangoPasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
