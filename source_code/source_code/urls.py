"""
ROOT URLS configuration 
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter
from users.views import CustomUserViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

router = SimpleRouter()
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
  path('admin/',                                admin.site.urls),

  path('',                                      include('dashboard.urls')),
  path('api/accounts/',                         include('accounts.urls')),
  
  path('api/v1/',                               include('api.urls')),
  path('api/schema/',                           SpectacularAPIView.as_view(),                                                            name='schema'),
  path('docs/',                                 SpectacularSwaggerView.as_view(url_name='schema'),                                       name='swagger-ui'),
  path('redoc/',                                SpectacularRedocView.as_view(url_name='schema'),                                         name='redoc'),

  path('activate/<uid>/<token>/',               TemplateView.as_view(template_name='activation.html'),                                   name='activation-page'),

  path('auth/',                                 include(router.urls)),
  path('auth/',                                 include('djoser.urls')),
  path('auth/',                                 include('djoser.urls.jwt')),
]
