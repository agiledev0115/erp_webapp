from django.shortcuts import render
from django.db.models.aggregates import Max
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from api import models, serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
import json

# Create your views here.

class UnitMeasureMVS(ModelViewSet):
    queryset = models.UnitMeasure.objects.all()
    serializer_class = serializers.UnitMeasureSerializer
    filter_fields = {
        'unit':['icontains', 'iregex', 'exact']
    }
    

class StatusMVS(ModelViewSet):
    queryset = models.Status.objects.all()
    serializer_class = serializers.StatusSerializer
    filter_fields = {
        'status':['icontains', 'iregex', 'exact']
    }

class PeopleMVS(ModelViewSet):
    queryset = models.People.objects.all()
    serializer_class = serializers.PeopleSerializer
    filter_fields = {
        'firstName':['icontains', 'iregex', 'exact'],
        'lastName':['icontains', 'iregex', 'exact'],
        'email':['icontains', 'iregex', 'exact'],
    }

class AttachmentMVS(ModelViewSet):
    queryset = models.Attachment.objects.all()
    serializer_class = serializers.AttachmentSerializer
    filter_fields = {
        'fileName':['icontains', 'iregex', 'exact'],
        'contentType':['icontains', 'iregex', 'exact'],
    }

    def create(self, request, *args, **kwargs):
        print(request.data)
        # print(">>>>>>>>>>>",request.data['attachedFile'].content_type)
        # print(">>>>>>>>>>>",request.data['attachedFile'].name)

        # print(">>>>>>>>>>>",dir(request.data['attachedFile']))
        data = request.data
        
        data['contentType']= request.data['attachedFile'].content_type
        data['fileName']= request.data['attachedFile'].name
            
        print(data)
        postSerializer = self.serializer_class(data= data, context={'request': request})

        if postSerializer.is_valid():
            postSerializer.save()
            return Response(data=postSerializer.data, status=HTTP_201_CREATED)
        else:
            return Response(data=postSerializer.errors, status=HTTP_500_INTERNAL_SERVER_ERROR)

class PartCategoryMVS(ModelViewSet):
    queryset = models.PartCategory.objects.all()
    serializer_class = serializers.PartCategorySerializer
    filter_fields = {
        'category':['exact','icontains','iregex']
    }

class SupplierMVS(ModelViewSet):
    queryset = models.Supplier.objects.all()
    serializer_class = serializers.SupplierSerializer
    filter_fields = {
        'name':['exact','icontains','iregex'],
        'poc__firstName':['exact','icontains','iregex'],
        'poc__lastName':['exact','icontains','iregex'],
        'address':['exact','icontains','iregex'],
    }

class PartMVS(ModelViewSet):
    queryset = models.Part.objects.all()
    serializer_class = serializers.PartSerializer
    filter_fields = {
        'name':['exact','icontains','iregex'],
        'category__category':['exact','icontains','iregex'],
        'supplier__name':['exact','icontains','iregex'],
    }


class MinimumStockMVS(ModelViewSet):
    queryset = models.MinimumStock.objects.all()
    serializer_class = serializers.MinimumStockSerializer
    filter_fields = {
        'part':['exact'],
        'part__name':['icontains', 'iregex', 'exact'],
        'part__category__category':['icontains', 'iregex', 'exact'],
        'minimumStock': ['exact','gt','lt','gte','lte'],
        'lastUpdateDate': ['exact','gt','lt','gte','lte']
    }

    def create(self, request, *args, **kwargs):
        # type checking of incoming request data to support multiple posting to API.
        # For single instance posting, incoming request.data is of type django queryset (Dict)
        # for multiple posting, incoming request.data type is array of dicts. !! add many=True in serializer line

        if all([isinstance(request.data, list), len(request.data) ==1]): 
            post_slr= self.serializer_class(data=request.data[0], context={"request":request})
        
        elif all([isinstance(request.data, list), len(request.data) > 1]): 
            post_slr = self.serializer_class(data=request.data, many=True, context={'request':request})

        else:
            post_slr= self.serializer_class(data=request.data, context={"request":request})


        if post_slr.is_valid():
            post_slr.save()
            return Response(data= post_slr.data, status=status.HTTP_201_CREATED)
        print(post_slr.errors)
        return Response(data=post_slr.errors, status= status.HTTP_400_BAD_REQUEST)

class CurrentStockMVS(ModelViewSet):
    queryset = models.CurrentStock.objects.all()
    serializer_class = serializers.CurrentStockSerializer
    filter_fields = {
        'part':['exact'],
        'part__name':['icontains', 'iregex', 'exact'],
        'part__category__category':['icontains', 'iregex', 'exact'],
        'currentStock': ['exact','gt','lt','gte','lte'],
        'lastUpdateDate': ['exact','gt','lt','gte','lte']
    }

    def create(self, request, *args, **kwargs):
        # type checking of incoming request data to support multiple posting to API.
        # For single instance posting, incoming request.data is of type django queryset (Dict)
        # for multiple posting, incoming request.data type is array of dicts. !! add many=True in serializer line

        if all([isinstance(request.data, list), len(request.data) ==1]): 
            post_slr= self.serializer_class(data=request.data[0], context={"request":request})
        
        elif all([isinstance(request.data, list), len(request.data) > 1]): 
            post_slr = self.serializer_class(data=request.data, many=True, context={'request':request})

        else:
            post_slr= self.serializer_class(data=request.data, context={"request":request})


        if post_slr.is_valid():
            post_slr.save()
            return Response(data= post_slr.data, status=status.HTTP_201_CREATED)
        print(post_slr.errors)
        return Response(data=post_slr.errors, status= status.HTTP_400_BAD_REQUEST)

class OrderMVS(ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

    filter_fields = {
        'part':['exact'],
        'poNumber': ['exact','gt','lt','gte','lte'],
        'part__name':['icontains', 'iregex', 'exact'],
        'part__category__category':['icontains', 'iregex', 'exact'],
        'quantity': ['exact','gt','lt','gte','lte'],
        'dateOrdered': ['exact','gt','lt','gte','lte'],
        'eta': ['exact','gt','lt','gte','lte'],
        'dateDelivered': ['exact','gt','lt','gte','lte'],
        'status': ['exact'],
        'unit__unit':['icontains', 'iregex', 'exact'],
    }

    def create(self, request, *args, **kwargs):
        # type checking of incoming request data to support multiple posting to API.
        # For single instance posting, incoming request.data is of type django queryset (Dict)
        # for multiple posting, incoming request.data type is array of dicts. !! add many=True in serializer line

        if all([isinstance(request.data, list), len(request.data) ==1]): 
            post_slr= self.serializer_class(data=request.data[0], context={"request":request})
        
        elif all([isinstance(request.data, list), len(request.data) > 1]): 
            post_slr = self.serializer_class(data=request.data, many=True, context={'request':request})

        else:
            post_slr= self.serializer_class(data=request.data, context={"request":request})


        if post_slr.is_valid():
            post_slr.save()
            return Response(data= post_slr.data, status=status.HTTP_201_CREATED)
        print(post_slr.errors)
        return Response(data=post_slr.errors, status= status.HTTP_400_BAD_REQUEST)

class ReceivingMVS(ModelViewSet):
    queryset = models.Receiving.objects.all()
    serializer_class = serializers.ReceivingSerializer
    filter_fields = {
        'orderItem':['exact'],
        'orderItem__poNumber':['icontains', 'iregex', 'exact'],
        'orderItem__part__name':['icontains', 'iregex', 'exact'],
        'quantity': ['exact','gt','lt','gte','lte'],
        'date': ['exact','gt','lt','gte','lte']
    }

class Dash(ModelViewSet):
    # modified method to get custom queryset for dashboard table in landing page
    # added filtering fuctionality using basic url parameters and ORM filtering
    serializer_class= serializers.DashSerializer 
    
    def get_queryset(self):
        sql="""
                SELECT * FROM
                    (SELECT parts_order.id, parts_order.name, ac.category, parts_order.onOrder FROM
                        (SELECT * FROM api_part AS ap
                        LEFT JOIN (SELECT part_id,
                                SUM(quantity) AS onOrder 
                                FROM api_order as ao 
                                GROUP BY part_id 
                                ORDER BY part_id) AS oq
                        ON ap.id = oq.part_id ORDER BY ap.id) as parts_order
                    LEFT JOIN api_partcategory AS ac 
                    ON ac.id = parts_order.category_id) part_category_order
                LEFT JOIN 
                    (SELECT cs.part_id, cs."currentStock", ms."minimumStock" FROM
                        (SELECT ac.part_id, ac."currentStock", csltd.latestdate FROM
                            (SELECT part_id, MAX("lastUpdateDate") AS latestdate FROM api_currentstock
                            GROUP BY part_id) AS csltd
                        JOIN api_currentstock as ac ON ac.part_id = csltd.part_id 
                        WHERE ac."lastUpdateDate" = csltd.latestdate ORDER BY ac.part_id) AS cs
                    JOIN 
                        (SELECT am.part_id, am."minimumStock", msltd.latestdate FROM
                            (SELECT part_id, MAX("lastUpdateDate") AS latestdate FROM api_minimumstock
                            GROUP BY part_id) AS msltd
                        JOIN api_minimumstock as am ON am.part_id = msltd.part_id 
                        WHERE am."lastUpdateDate" = msltd.latestdate ORDER BY am.part_id) AS ms
                    ON
                    cs.part_id = ms.part_id) current_min
                ON
                current_min.part_id = part_category_order.id
                """
        
        queryset= models.PartCategory.objects.raw(raw_query=sql)
        return queryset

    def create(self, request):
        response = {'message': 'Create function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None):
        response = {'message': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        response = {'message': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        response = {'message': 'Delete function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
