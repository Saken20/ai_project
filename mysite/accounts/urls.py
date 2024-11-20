from accounts import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path('', views.accounts, name='accounts'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('logout/', views.logout, name='logout' ),
    path('profile/', views.profile, name='profile'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)