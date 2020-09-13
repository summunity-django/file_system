"""
File System Models
====================

The file system models are used for storing and retrieving data
from the media directory

:Author: Nik Sumikawa
:Date: Aug 21, 2020
"""



from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

import logging

# class File(models.Model):
#     """ exception Model definition """
#
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     file = models.FileField(upload_to='test_dir')
#
#     def __str__(self):
#         return self.file
