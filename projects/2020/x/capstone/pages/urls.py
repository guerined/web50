from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('faq/', views.faq, name='faq'),
    path('cookies/', views.cookies, name='cookies'),
    path('contract/', views.contract, name='contract'),
    path('privacy/', views.privacy, name='privacy'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('contact/', views.contact, name='contact'),
    path("logout/", views.logout_view, name="logout"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('qr/<str:shortened_part>',
         views.redirect_url_view, name='redirect_url_view'),
    path('delete/<int:qr_id>', views.delete, name='delete'),
]
