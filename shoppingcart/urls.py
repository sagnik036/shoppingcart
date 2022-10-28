from django.contrib import admin
from django.urls import path,include
from . import settings
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('api.products.urls')),
    path('api/',include('api.usercart.urls')),
    path('authenticate/',include('api.users.urls')),
    path('authenticate/login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair')
]
urlpatterns+=static(settings.MEDIA_URL ,document_root = settings.MEDIA_ROOT)