from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('food/', include('food.urls')),
    # path('account/', include('account.urls')),
    # path('recipies/', include('recipies.urls')),
    # path('user_rating/', include('user_rating.urls')),
]
