from django.shortcuts import render, redirect
from django.views.generic import FormView, UpdateView
from .forms import UserRegistrationForm,  UserUpdateForm, User
from django.contrib.auth.forms import AuthenticationForm , PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout ,update_session_auth_hash
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.
class UserRegistrationView(FormView):
        template_name = 'accounts/user_registration.html'
        form_class = UserRegistrationForm
        success_url = reverse_lazy('login')

        def form_valid(self, form):
            print(form.cleaned_data)
            user = form.save()
        #  login(self.request, user)     # sob data thik thakle login koraya felbe
            # print(user)
            return super().form_valid(form)
    

class UserUpdateProfile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/profile.html'

    def get_object(self):
        return self.request.user   # Logged-in user ke object hisebe return kortese

    def get_success_url(self):
        return reverse_lazy('profile')




def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request = request, data = request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username = username, password = password)
                if user is not None:
                    login(request,user)
                    return redirect('home')
        else:
            form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})
    else:
        return redirect('home')
                 

# def profile(request): 
#     if request.user.is_authenticated:
#        return render(request, 'accounts/profile.html')
#     else:
#         return redirect('login')

def user_logout(request): 
    logout(request)
    return redirect('login')