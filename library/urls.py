"""
URL configuration for library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
# from rest_framework.response import Response
# from rest_framework.decorators import api_view


# @api_view(['GET'])
# def api_root(request):
#     return Response({
#         "message": "Welcome to the Library Management System API.",
#         "endpoints": {
#             "Register": "/auth/register/",
#             "Login": "/auth/login/",
#             "Reset Password": "/auth/password/reset/",
#             "Logout": "/auth/logout/",
#             "Add Book": "/auth/books/",
#             "Update Book": "/auth/books/<id>/",
#             "Borrow Book": "/borrow/",
#             "Return Book": "/return/",
#             "Reserve Book": "/reserve/",
#             "Renew Book": "/renew/",
#             "Borrow History": "/history/",
#             "Cancel Reservation": "/cancel/<id>/",
#             "Fines": "/fines/",
#             "Payments": "/payments/"
#         }
#     })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    # path('', api_root),
]
