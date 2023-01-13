from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import View


# Create your views here.
# class PremisLoginView(LoginView):
#     template_name = "login/login.html"
    
#     redirect_authenticated_user = True


class PremisLoginView(View):
    template_name = 'login/login.html'
    form_class = AuthenticationForm

    def get(self, request):
        form = self.form_class
        message = ''
        return render(request, self.template_name, context={ 'form':form, 'message':message})
    
    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('index')
        
        message = 'Login failed'
        return render(request, self.template_name, context={'form':form, 'message':message})


class PremisLogout(LogoutView):
    template_name = 'login/logout.html'
