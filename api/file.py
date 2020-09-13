"""
File System REST API
=============================

Interface for storing and retrieving data from the file system

:Author: Nik Sumikawa
:Date: Aug 21, 2020
"""

import logging
log = logging.getLogger(__name__)

from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf.urls import url
from django.db.models import Q, F

from employee.models import *

from django_config.request_params import request_params
from django_config.rest_framework import RestFramework
from django_config.doc_framework import DocumentationSchema
from employee.driver.user_info import UserInfoAPI

from rest_framework import status


class DocSchema(DocumentationSchema):
    """
    Overrides `get_link()` to provide Custom Behavior X
    """
    def __init__( self ):
        super().__init__()

        # from docs.rest.product.product import parameters, properties
        self.tags =  ['File System']
        # self.parameters = parameters.parameters
        # self.properties = properties.properties



class FileSystemAPI(RestFramework):

    schema = DocSchema()

    # def get(self, request):
    #     """ returns information about the specified set of products """
    #
    #     # parse the parameter from the request
    #     params = request_params(request)
    #
    #     print( params )
    #     # user the python API to add and remove products
    #     python_api = UserInfoAPI()
    #
    #     product_objects = python_api.get_products(core_id=params['core_id'])
    #
    #     # return a queryset containing products assigned to the employee
    #     return Response( data=product_objects.values() )

    def put(self, request):
        """ add a single file to the media directory """

        import os
        from django_config.settings import MEDIA_ROOT

        data = dict(request.data)

        # create a custom directory to store the document. Allow for a default
        directory = 'default'
        if 'directory' in data.keys(): directory = data['directory'][0]

        path = '%s/%s/' % (MEDIA_ROOT,  directory)
        if not os.path.exists(path): os.makedirs(path)

        file_obj = request.FILES['file']
        file_location = open(path + file_obj.name, 'wb+')
        for chunk in file_obj.chunks():
            file_location.write(chunk)
            file_location.close()

        return Response(data={
            'error': False,
            'url': path + file_obj.name,
            })


    def post(self, request):
        """ adds a single or multiple files to the media directory (prefered option) """

        import os
        from django_config.settings import MEDIA_ROOT

        data = dict(request.data)

        # create a custom directory to store the document. Allow for a default
        directory = 'default'
        if 'directory' in data.keys(): directory = data['directory'][0]

        path = '%s/%s/' % (MEDIA_ROOT,  directory)
        if not os.path.exists(path): os.makedirs(path)

        for file_ref in request.FILES:

            file_obj = request.FILES[file_ref]

            file_location = open(path + file_obj.name, 'wb+')
            for chunk in file_obj.chunks():
                file_location.write(chunk)
                file_location.close()

        url =  ['%s/%s' % (directory, request.FILES[ref].name) for ref in request.FILES]

        return Response(
            data={
                'error': 'False',
                'url': ','.join(url),
                },
            )


# file_obj = request.FILES['file']
    #
    # def delete(self, request):
    #     """ add or updates product objects """
    #
    #     import json
    #
    #     # parses the json object from the body of the post request
    #     body_unicode = request.body.decode('utf-8')
    #     body = json.loads(body_unicode)
    #
    #
    #     if 'core_id' not in body.keys():
    #         log.warn( 'user id is required for assign a product')
    #         return Response(data={'error': True})
    #
    #     python_api = UserInfoAPI()
    #     python_api.remove_product( **body )
    #
    #     product_objects = python_api.get_products(core_id=body['core_id'])
    #
    #     return Response( data=product_objects.values() )
    #
    #
    # def query_parameters( self, variable, var_list ):
    #     """ returns a dictionary containing all queryset parameters """
    #
    #     return {
    #         'id': Q(id__in = var_list ),
    #         'fab_id': Q(technology__fab__in = var_list ),
    #         'tech_id': Q(technology__in = var_list ),
    #         'fab': Q(technology__fab__name__in = var_list ),
    #         'tech': Q(technology__name__in = var_list ),
    #         'business': Q(business__in = var_list ),
    #         'active': Q(active = variable ),
    #     }
    #


urlpatterns = [url(r'^files$', FileSystemAPI.as_view(), name='FileSystemAPI')]
