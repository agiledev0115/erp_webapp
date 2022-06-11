from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from frontend import views


app_name = 'frontend'

urlpatterns = [
    path('logout', views.logoutRedirect, name='logoutRedirect'),
    path('', views.HomePage.as_view(), name='home'),
    path('current', views.CurrentStock.as_view(), name='currentHome'),
    path('current/update', views.CurrentStockUpdate.as_view(), name='currentUpdate'),
    path('current/upload', views.CurrentStockUpload.as_view(), name='currentUpload'),
    path('min', views.MinimumStock.as_view(), name='minHome'),
    path('min/update', views.MinStockUpdate.as_view(), name='minUpdate'),
    path('min/upload', views.MinimumStockUpload.as_view(), name='minUpload'),
    path('purchasing', views.Purchasing.as_view(), name='purchasingHome'),
    path('purchasing/create', views.PurchasingCreate.as_view(), name='purchasingCreate'),
    path('purchasing/update/<int:pk>', views.PurchaseUpdate.as_view(), name='purchasingUpdate'),
    path('purchasing/close',views.ClosePurchaseOrder.as_view(), name='purchasingClose' ),
    path('purchasing/open/<int:pk>',views.OpenPurchaseOrder.as_view(), name='purchasingOpen' ),
    path('purchasing/delete', views.DeletePurchaseOrder.as_view(), name='purchaseDelete'),
    path('purchasing/edit', views.EditPurchaseOrder.as_view(), name='purchaseEdit'),

    path('workingonit', TemplateView.as_view(template_name='inprogress/underWork.html'), name='inprog')

    # path('test',(TemplateView.as_view(template_name='registration/login_test.html')), name='test'),
    # path('workingonit', TemplateView.as_view(template_name='inprogress/underWork_normal.html'), name='inprog')
]