"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from certificate import views
from django.views.generic import TemplateView


urlpatterns = [
    path('swagger-ui', TemplateView.as_view(
      template_name='swagger-ui.html',
      extra_context={'schema_url': 'reqParse'}
    ), name='swagger-ui'),
    path('certificate/parsing', views.CertificateParsing.as_view(), name='crtParse'),
    path('certificate/signing', views.CertificateSigning.as_view(), name='crtSign'),
    path('certificate/making', views.CertificateMaking.as_view(), name='crtMake'),
    path('certificate/files', views.CertificateFiles.as_view(), name="crtFiles"),
    re_path(r'^certificate/file/(?P<filename>)(?P<style>)', views.CertificateFile.as_view(), name='crtFile'),
]
