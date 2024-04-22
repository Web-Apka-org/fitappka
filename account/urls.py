from django.urls import path, include
from .views import UserLoginView, RegisterPage, UserData, UserLogoutView, UserUpdate, UserPage

urlpatterns = [
     path('', UserData.as_view(), name = 'user_data'), 
     path('<int:pk>/', UserPage.as_view(), name = 'user_page'),
     path('login/', UserLoginView.as_view(), name = 'login_user'),
     path('logout/', UserLogoutView.as_view(next_page = 'login_user'), name = 'logout_user'),
     path('signup/', RegisterPage.as_view(), name = 'signup_user'),
     path('update/<int:pk>', UserUpdate.as_view(), name = 'update_user'),
     path('summary/',include('summary.urls')),
 ]
