from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('',                                        TemplateView.as_view(template_name='login.html'),                                                 name="login"),
    path('dashboard/homepage',                      TemplateView.as_view(template_name='dashboard.html')),
    path("register/",                               TemplateView.as_view(template_name="register.html"),                                              name="register"),
    path('profile/',                                TemplateView.as_view(template_name='profilo_section/profilo.html'),                               name='profile-page'),
]
