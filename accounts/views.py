from django.shortcuts import render, redirect
from django.views.generic import FormView, UpdateView
from .forms import UserRegistrationForm,  UserUpdateForm, User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout 
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.core.mail import send_mail



# Create your views here.
class UserRegistrationView(FormView):
        template_name = 'accounts/user_registration.html'
        form_class = UserRegistrationForm
        success_url = reverse_lazy('login')

        def form_valid(self, form):
            print(form.cleaned_data)
            user = form.save()
            #login(self.request, user)     # sob data thik thakle login koraya felbe
            # print(user)
            messages.success(self.request, "Account created successfully! Please login.")
            return super().form_valid(form)
    

class UserUpdateProfile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/profile.html'

    def get_object(self):
        return self.request.user   # Logged-in user ke object hisebe return kortese

    def get_success_url(self):
        messages.success(self.request, "Profile updated successfully!")
        return reverse_lazy('profile')




def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('profile')
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

                 

# def profile(request): 
#     if request.user.is_authenticated:
#        return render(request, 'accounts/profile.html')
#     else:
#         return redirect('login')

def user_logout(request): 
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')


class ChangePassView(LoginRequiredMixin,PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        send_mail(
            subject="Password Changed Successfully",
            message="Hello, your password has been successfully changed.",
            from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings.py
            recipient_list=[self.request.user.email],
            fail_silently=False,
        )
        messages.success(self.request, "Your password is successfully changed.")
        return super().form_valid(form)