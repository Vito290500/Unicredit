from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('',                                        TemplateView.as_view(template_name='login.html'),                                                 name="login"),
    path('dashboard/homepage',                      TemplateView.as_view(template_name='dashboard.html'),                                             name="homepage"),
    path("register/",                               TemplateView.as_view(template_name="register.html"),                                              name="register"),
    path('profile/',                                TemplateView.as_view(template_name='profilo_section/profilo.html'),                               name='profile-page'),
    path('profile/gestisci_account',                TemplateView.as_view(template_name='profilo_section/gestisci_account.html'),                      name='gestisci-account'),
    path('profile/dati_personali',                  TemplateView.as_view(template_name='profilo_section/dati_personali.html'),                        name='dati-personali'),
]
