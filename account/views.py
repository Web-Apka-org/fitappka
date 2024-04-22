from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import LogoutView

from .serializers import UserSerializer
from .models import User

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import SignupForm, LoginForm


class RegisterPage(FormView):
    template_name = "register.html"
    form_class = SignupForm
    success_url = reverse_lazy('login_user')
    serializer_class = UserSerializer

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class UserLoginView(View):
    form_class = LoginForm
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        status = True
        form = self.form_class(request.POST)
        if form.is_valid:
            username = form.data['username']
            password = form.data['password']
            user = authenticate(request, username=username, password=password)
            status_code = 404 if status else 200
            if user:
                login(request, user)
                return redirect('user_data')
            elif user is None:
                return render(request, self.template_name, {'form': form, 'status': status} ,status = status_code)


        return render(request, self.template_name, {'form': form})
    
class UserLogoutView(LogoutView):
    template_name = 'index.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('login_user')

class UserData(APIView):
    model = User
    context_object_name = 'user_data'
    template_name = 'index.html'
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            id = self.request.user.id
            if id == self.request.user.id:
                user = User.objects.filter(id = self.request.user.id)
                serializer = UserSerializer(user, many = True)
                return Response(serializer.data)
            else:
                return Response({'error': 'You do not have permission to view this user data.'}, status=403)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

class UserPage(LoginRequiredMixin, ListView):
    model = User
    fields = '__all__'
    context_object_name = 'user_data'
    template_name = 'index.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_data'] = context['user_data'].filter(id = self.request.user.id)

        return context
    
class UserUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'user_form.html'
    model = User
    fields = ['username', 'email']
    success_url = reverse_lazy('user_data')