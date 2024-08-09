from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/', accounts_views.signup_view, name='signup'),
    path('accounts/login/', accounts_views.login_view, name='login'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('accounts/password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('accounts/password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    path('accounts/save_reading/', accounts_views.save_reading, name='save_reading'),
    path('accounts/electricity/', accounts_views.electricity, name='electricity'),
    path('accounts/', include('allauth.urls')),
    path('accounts/upload/', accounts_views.upload_meter_reading, name='upload_meter_reading'),
    path('accounts/success/', accounts_views.success, name='success'),
    path('accounts/account/', accounts_views.account, name='account'),
    
    path('', accounts_views.home, name='home'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)