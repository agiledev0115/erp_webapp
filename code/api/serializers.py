from rest_framework.serializers import HyperlinkedModelSerializer, Serializer, IntegerField, CharField
from api import models

class UnitMeasureSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.UnitMeasure
        fields = '__all__'
        extra_kwargs = {
            'url' : {'view_name': 'api:unitmeasure-detail'}
        }


class StatusSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.Status
        fields = '__all__'
        extra_kwargs = {
            'url' : {'view_name': 'api:status-detail'}
        }

class PeopleSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.People
        fields = '__all__'
        extra_kwargs = {
            'url' : {'view_name': 'api:people-detail'}
        }

class AttachmentSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.Attachment
        fields = '__all__'
        extra_kwargs = {
            'url' : {'view_name': 'api:attachment-detail'}
        }

class PartCategorySerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.PartCategory
        fields = '__all__'
        extra_kwargs ={
            'url':{'view_name':'api:partcategory-detail'}
        }

class SupplierSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = models.Supplier
        fields = '__all__'
        extra_kwargs = {
            'url':{'view_name':'api:supplier-detail'},
            'poc':{'view_name':'api:people-detail'}
        }

class PartSerializer(HyperlinkedModelSerializer):
    
    class Meta:
        model = models.Part
        fields='__all__'
        extra_kwargs ={
            'url': {'view_name':'api:part-detail'},
            'category':{'view_name':'api:partcategory-detail'},
            'supplier' :{'view_name':'api:supplier-detail'},
            'unit' :{'view_name':'api:unitmeasure-detail'}

        }



class MinimumStockSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.MinimumStock
        fields = '__all__'
        extra_kwargs = {
            'url' : {'view_name': 'api:minstock-detail'},
            'part': {'view_name': 'api:part-detail'},
        }

class CurrentStockSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.CurrentStock
        fields = '__all__'
        extra_kwargs = {
            'url' : {'view_name': 'api:currentstock-detail'},
            'part': {'view_name': 'api:part-detail'},
        }

class OrderSerializer(HyperlinkedModelSerializer):

    class Meta:
        model= models.Order
        fields= (
            'url',
            'id',
            'poNumber',
            'part',
            'quantity',
            'received',
            'unit',
            'dateOrdered',
            'eta',
            'dateDelivered',
            'status'
        )
        extra_kwargs = {
            'url':{'view_name':'api:order-detail'},
            'part':{'view_name':'api:part-detail'},
            'unit':{'view_name':'api:unitmeasure-detail'},
            'status':{'view_name':'api:status-detail'}
        }

class ReceivingSerializer(HyperlinkedModelSerializer):

    class Meta:
        model= models.Receiving
        fields='__all__'
        extra_kwargs = {
            'url':{'view_name':'api:receiving-detail'},
            'orderItem':{'view_name':'api:order-detail'},
            'attachment':{'view_name':'api:attachment-detail'}
        }

class DashSerializer(Serializer):
    id = IntegerField()
    name = CharField()
    category = CharField()
    onorder = IntegerField()
    currentStock = IntegerField()
    minimumStock = IntegerField()