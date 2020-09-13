"""
File System URL
====================

url patterns for the file system interface

:Author: Nik Sumikawa
:Date: Aug 21, 2020
"""

from rest_framework.routers import DefaultRouter

from django.urls import path
from django.conf.urls import url

from file_system import api


router = DefaultRouter()
urlpatterns = router.urls

urlpatterns += api.urlpatterns
