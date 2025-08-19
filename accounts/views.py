from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm, UserUpdateForm
from .models import CustomUser

class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user