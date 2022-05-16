from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
# from rest_framework.aut
from api import views

app_name = 'api'

router = DefaultRouter()

router.register('unitmeasure', viewset=views.UnitMeasureMVS, basename='unitmeasure')
router.register('status', viewset=views.StatusMVS, basename='status')
router.register('people', viewset=views.PeopleMVS, basename='people')
router.register('attachment', viewset=views.AttachmentMVS, basename='attachment')
router.register('partcategory', viewset=views.PartCategoryMVS, basename='partcategory')
router.register('supplier', viewset=views.SupplierMVS, basename='supplier')
router.register('part',viewset=views.PartMVS, basename='part')
router.register('minstock', viewset=views.MinimumStockMVS, basename='minstock')
router.register('currentstock', viewset=views.CurrentStockMVS, basename='currentstock')
router.register('order', viewset=views.OrderMVS, basename='order')
router.register('receiving', viewset=views.ReceivingMVS, basename='receiving')
router.register('dash', viewset=views.Dash, basename='dash')

urlpatterns = [
    path('', include(router.urls)),
    path('schema', get_schema_view(title='ERP API', description='RESTful API for the ERP web application'))
]

from rest_framework.authtoken import views
urlpatterns += [
    path('auth-token/', views.obtain_auth_token)
]