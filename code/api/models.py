from typing import OrderedDict
from django.db import models


# Create your models here.
class UnitMeasure(models.Model):
    """
    Unit of measurements
    """
    id = models.AutoField(primary_key=True)
    unit = models.CharField(max_length=50 ,null=False)

    def __str__(self) -> str:
        return self.unit

class Status(models.Model):
    """
    status codes
    """
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50 ,null=False)

    def __str__(self) -> str:
        return self.status

class People(models.Model):
    """
    people names and contact
    """
    id = models.AutoField(primary_key= True)
    firstName = models.CharField(max_length=150)
    lastName = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)

    def __str__(self) -> str:
        return f"{self.firstName} {self.lastName}"

class Attachment(models.Model):
    """
    Attachments for receieving
    """
    id = models.AutoField(primary_key=True)
    fileName = models.CharField(null=True, max_length=150)
    attachedFile = models.FileField(null=False, upload_to='media/')
    contentType = models.CharField(max_length=150, null=True)
    dateOfUpload = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.fileName}.{self.contentType}"


class PartCategory(models.Model):
    """
    part category for parts
    """
    id=models.AutoField(primary_key=True)
    category = models.CharField(max_length=150 ,verbose_name="part category", null=False)

    def __str__(self) -> str:
        return self.category



class Supplier(models.Model):
    """
    Supplier information
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150 ,null=False)
    poc = models.ForeignKey(People, on_delete= models.deletion.CASCADE, related_name='supplierPoc', null=True, unique=False)
    address = models.CharField(max_length=300, help_text="Enter full address with country", null=True)

    def __str__(self) -> str:
        return self.name

class Part(models.Model):
    """
    Part details
    """
    id= models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, null=False)
    category = models.ForeignKey(PartCategory, on_delete=models.deletion.CASCADE, related_name='partCategoryFk')
    supplier = models.ForeignKey(Supplier, on_delete=models.deletion.CASCADE, related_name='supplierFk', null=True)
    unit = models.ForeignKey(UnitMeasure, on_delete=models.deletion.CASCADE, related_name='partUnitFk', default=4)

    def __str__(self) -> str:
        return self.name

class MinimumStock(models.Model):
    """
    Minimum stocking level for inventory
    """
    id = models.AutoField(primary_key=True)
    part = models.ForeignKey(Part, on_delete=models.deletion.CASCADE, related_name= "minStockPart")
    minimumStock = models.PositiveIntegerField(null=False)
    lastUpdateDate = models.DateTimeField(auto_now=True)


class CurrentStock(models.Model):
    """
    Current stock levels held in inventory
    """
    id = models.AutoField(primary_key=True)
    part = models.ForeignKey(Part, on_delete=models.deletion.CASCADE, related_name='CurrentStockPart')
    currentStock = models.PositiveIntegerField(null=False)
    lastUpdateDate = models.DateTimeField(auto_now=True)

class Order(models.Model):
    """
    Purchase orders for parts
    """
    id = models.AutoField(primary_key=True)
    poNumber = models.PositiveIntegerField(null=False)
    part = models.ForeignKey(Part, on_delete=models.deletion.CASCADE, related_name='orderPart')
    quantity = models.PositiveIntegerField(null=False)
    received = models.PositiveIntegerField(default=0)
    unit = models.ForeignKey(UnitMeasure, on_delete=models.deletion.CASCADE, related_name='unitFk')
    dateOrdered = models.DateField(null=False)
    eta = models.DateField(null=False)
    dateDelivered = models.DateField(null=True)
    status = models.ForeignKey(Status ,default=False, help_text="order status, true-> delivered, false-> incomplete", on_delete=models.deletion.CASCADE, related_name='orderStatus')

    def __str__(self) -> str:
        return f"po#:{self.poNumber}/part:{self.part}/ordered:{self.quantity}"

    class Meta:
        ordering=['id',]


class Receiving(models.Model):
    """
    for receieving attachements like packing slips, invoice etc
    """
    id= models.AutoField(primary_key=True)
    orderItem = models.ForeignKey(Order, on_delete=models.deletion.CASCADE, related_name='receivingOrder')
    quantity = models.PositiveIntegerField(null=False)
    attachment = models.ForeignKey(Attachment, on_delete=models.deletion.CASCADE, related_name='receivingAttachment', null=True)
    date= models.DateField(auto_now=True)