import requests
from utils.utils import csvread
import json
import time
from django.urls import reverse, resolve, reverse_lazy
# from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from utils.apiUtils import api_get, api_auth, api_post, api_patch, api_delete
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
decorators=[never_cache,]

# Create your views here.


def logoutRedirect(request):
    # print(request)
    logout(request=request)
    
    return HttpResponseRedirect(redirect_to=reverse('frontend:home'))

# Homepage

class HomePage(LoginRequiredMixin, View):
    # redirect_field_name = 'redirect_to'
    template_name = 'home/dash.html'
    dashEndpoint = reverse_lazy('api:dash-list')
    typeEndpoint = reverse_lazy('api:partcategory-list')

    def get(self,request):

        dashUrl = request.build_absolute_uri(self.dashEndpoint)
        dashGet = api_get(url= dashUrl, request= request)
        # print(dashGet.status_code)

        typeUrl = request.build_absolute_uri(self.typeEndpoint)
        typeGet = api_get(url=typeUrl, request=request)

        if isinstance(dashGet, HttpResponse):
            return dashGet
        if isinstance(typeGet, HttpResponse):
            return typeGet


        data ={'dash':dashGet.json(), 'types':typeGet.json(), 'module':'Dashboard'}
        
        return render(request, template_name=self.template_name, context=data)

class CurrentStock(LoginRequiredMixin, View):
    template_name = 'current/current.html'
    dashEndpoint = reverse_lazy('api:dash-list')
    typeEndpoint = reverse_lazy('api:partcategory-list')
    

    def get(self,request):

        dashUrl = request.build_absolute_uri(self.dashEndpoint)
        dashGet = api_get(url= dashUrl, request= request)
        # print(dashGet.status_code)

        typeUrl = request.build_absolute_uri(self.typeEndpoint)
        typeGet = api_get(url=typeUrl, request=request)

        if isinstance(dashGet, HttpResponse):
            return dashGet
        if isinstance(typeGet, HttpResponse):
            return typeGet

       

        data ={
            'dash':dashGet.json(),
            'types':typeGet.json(),
            'module':'Current Stock'}
        
        return render(request, template_name=self.template_name, context=data)

class CurrentStockUpdate(LoginRequiredMixin, View):

    def get(self,request):
        return redirect(to=reverse_lazy('frontend:currentHome'))

    def post(self,request):

        partUrl = request.build_absolute_uri(reverse_lazy('api:part-list'))
        partGet = api_get(url= partUrl, request= request)
        partData = partGet.json()

        updateQuantity = request.POST.getlist('new_quantity')

        apiPostData = []

        for count,val in enumerate(updateQuantity):
            if val != "":
                apiPostData.append({
                    'part': partData[count]['url'],
                    'currentStock': int(val)
                })

        currentStockUrl = request.build_absolute_uri(reverse_lazy('api:currentstock-list'))

        apiPost =api_post(
            url= currentStockUrl,
            data=json.dumps(apiPostData),
            request=request,
            post_content_type='json'
            )
        
        if isinstance(apiPost, HttpResponse):
            return apiPost

        return redirect(to=reverse_lazy('frontend:currentHome'))

class CurrentStockUpload(LoginRequiredMixin, View):

    def post(self,request):
        
        reader = csvread(request=request,form_handle='file')
        current_post = []
        for row in reader:
            if row[2] != "":
                current_post.append(
                {
                    "part": row[0],
                    "currentStock": row[2]
                }
                )
        current_post.pop(0)
        # print(json.dumps(current_post))
        
        api = request.build_absolute_uri(reverse_lazy('api:currentstock-list'))
        
        apiPost = api_post(url= api, request=request, data= json.dumps(current_post), post_content_type='json')

        if isinstance(apiPost, HttpResponse):
            return apiPost

        return redirect(to=reverse_lazy('frontend:currentHome'))


class MinimumStock(LoginRequiredMixin, View):
    template_name = 'min/min.html'
    dashEndpoint = reverse_lazy('api:dash-list')
    typeEndpoint = reverse_lazy('api:partcategory-list')

    def get(self,request):

        dashUrl = request.build_absolute_uri(self.dashEndpoint)
        dashGet = api_get(url= dashUrl, request= request)
        # print(dashGet.status_code)

        typeUrl = request.build_absolute_uri(self.typeEndpoint)
        typeGet = api_get(url=typeUrl, request=request)

        if isinstance(dashGet, HttpResponse):
            return dashGet
        if isinstance(typeGet, HttpResponse):
            return typeGet


        data ={'dash':dashGet.json(), 'types':typeGet.json(), 'module':'Minimum Stock'}
        
        return render(request, template_name=self.template_name, context=data)

class MinStockUpdate(LoginRequiredMixin, View):

    def get(self,request):
        return redirect(to=reverse_lazy('frontend:minHome'))

    def post(self,request):
        # print(request.POST)

        partUrl = request.build_absolute_uri(reverse_lazy('api:part-list'))
        partGet = api_get(url= partUrl, request= request)
        partData = partGet.json()

        updateQuantity = request.POST.getlist('new_quantity')

        apiPostData = []

        for count,val in enumerate(updateQuantity):
            if val != "":
                apiPostData.append({
                    'part': partData[count]['url'],
                    'minimumStock': int(val)
                })

        # print(apiPostData)
        minStockUrl = request.build_absolute_uri(reverse_lazy('api:minstock-list'))

        apiPost =api_post(
            url= minStockUrl,
            data=json.dumps(apiPostData),
            request=request,
            post_content_type='json'
            )
        
        if isinstance(apiPost, HttpResponse):
            return apiPost

        return redirect(to=reverse_lazy('frontend:minHome'))

class MinimumStockUpload(LoginRequiredMixin, View):

    def post(self,request):
        
        reader = csvread(request=request,form_handle='file')
        current_post = []
        for row in reader:
            if row[2] != "":
                current_post.append(
                {
                    "part": row[0],
                    "minimumStock": row[2]
                }
                )
        current_post.pop(0)
        # print(json.dumps(current_post))
        
        api = request.build_absolute_uri(reverse_lazy('api:minstock-list'))
        
        apiPost = api_post(url= api, request=request, data= json.dumps(current_post), post_content_type='json')

        if isinstance(apiPost, HttpResponse):
            return apiPost

        return redirect(to=reverse_lazy('frontend:minHome'))


class Purchasing(LoginRequiredMixin, View):
    template_name= 'purchasing/main.html'
    dashEndpoint = reverse_lazy('api:dash-list')
    typeEndpoint = reverse_lazy('api:partcategory-list')
    orderEndpoint = reverse_lazy('api:order-list')

    def get(self, request):
        dashUrl = request.build_absolute_uri(self.dashEndpoint)
        dashGet = api_get(url= dashUrl, request= request)
        # print(dashGet.status_code)

        typeUrl = request.build_absolute_uri(self.typeEndpoint)
        typeGet = api_get(url=typeUrl, request=request)

        orderUrl = request.build_absolute_uri(self.orderEndpoint)
        orderGet = api_get(url=orderUrl, request=request)

        if isinstance(dashGet, HttpResponse):
            return dashGet
        if isinstance(typeGet, HttpResponse):
            return typeGet
        if isinstance(orderGet, HttpResponse):
            return orderGet

        orderData = orderGet.json()

        
        total = len(orderData)
        delivered = 0
        undelivered =0
        for order in orderData:
            if order['dateDelivered']:
                delivered +=1
            elif order['dateDelivered'] is None:
                undelivered +=1
        
        orderSummary={
            'total' : total,
            'delivered' : delivered,
            'undelivered' : undelivered
        }


        data ={'dash':dashGet.json(), 'types':typeGet.json(), 'summary':orderSummary, 'module':'Purchasing'}
        
        return render(request, template_name=self.template_name, context=data)

@method_decorator(name='dispatch', decorator=never_cache)
class PurchasingCreate(LoginRequiredMixin,View):
    template_name = 'purchasing/createMain.html'
    orderEndpoint = reverse_lazy('api:order-list')
    partEndpoint = reverse_lazy('api:part-list')

    def get(self,request, extra=None):

        startTime = time.time()
        partUrl = request.build_absolute_uri(self.partEndpoint)
        partGet = api_get(url= partUrl, request=request)

        orderUrl = request.build_absolute_uri(self.orderEndpoint)
        orderGet =api_get(url=orderUrl, request=request)


        if isinstance(partGet, HttpResponse):
            return partGet

        if isinstance(orderGet, HttpResponse):
            return orderGet
        
        partData = partGet.json()
        orderData = orderGet.json()

        for dict in orderData:
            for pdict in partData:
                if pdict['url']== dict['part']:
                    dict['partName']= pdict['name']
            # print(dict['partName'])                

        
        data={
            'parts': partData,
            'orders': orderData
        }

        # print('!!!!!>>> Time: ', (time.time()-startTime))
        return render(request=request, template_name= self.template_name, context=data)
    
    def post(self,request):

        # print(request.POST)

        incomingPostData = request.POST

        apiPostData =[]

        partData = incomingPostData.getlist("part")
        quantityData = incomingPostData.getlist("quantity")
        

        for count,part in enumerate(partData):
            # print(count, part)
            apiPostData.append({
                "poNumber": incomingPostData["ponumber"],
                "quantity": quantityData[count],
                "dateOrdered": incomingPostData["date_ordered"],
                "eta": incomingPostData["eta"],
                "part": part,
                "unit": "http://127.0.0.1:8000/api/unitmeasure/4/",
                "status": "http://127.0.0.1:8000/api/status/1/"
            })

        # print(apiPostData)
        orderUrl = request.build_absolute_uri(self.orderEndpoint)
        orderPost = api_post(url=orderUrl,request=request,data= json.dumps(apiPostData), post_content_type="json")

        if isinstance(orderPost, HttpResponse):
            return orderPost

        

        return self.get(request=request)

class PurchaseUpdate(LoginRequiredMixin,View):
    template_name = 'purchasing/update.html'
    partEndpoint = reverse_lazy('api:part-list')
    attachmentEndpoint = reverse_lazy('api:attachment-list')
    currentEndpoint =reverse_lazy('api:currentstock-list')
    receivingEndpoint = reverse_lazy('api:receiving-list')


    reverse_lazy('api:currentstock-list')



    def get(self,request,pk):
        orderEndpoint = reverse_lazy('api:order-detail' , kwargs={'pk':pk} )
        orderUrl = request.build_absolute_uri(orderEndpoint)
        orderGet = api_get(url=orderUrl,request=request)

        if isinstance(orderGet, HttpResponse):
            return orderGet

        partListUrl = request.build_absolute_uri(self.partEndpoint)
        partListGet = api_get(url=partListUrl,request=request)

        if isinstance(partListGet, HttpResponse):
            return partListGet

        orderData = orderGet.json()
        partUrl = orderData['part']
        partGet =api_get(url=partUrl, request=request)

        if isinstance(partGet, HttpResponse):
            return partGet
        
        partData = partGet.json()

        data = {
            'order': orderData,
            'part': partData,
            'partlist': partListGet.json()
        }

        return render(request, template_name=self.template_name, context=data)

    def post(self,request, pk):

        # print(request.POST)
        incomingData = request.POST
        
        # Check if any attachement is given and post to api,
        # on successful posting of attachment, get url of the attachment
        if request.FILES:
            # print('@@!!',request.FILES)
            # attachment =request.FILES
            attachmentUrl = request.build_absolute_uri(self.attachmentEndpoint)
            # print(attachmentUrl)

            attachmentPost= api_post(request=request ,url=attachmentUrl, files={'attachedFile': request.FILES['r_attachment']})
            # print('##!!>>', type(attachmentPost.content))

            if isinstance(attachmentPost, HttpResponse):
                return attachmentPost
            
            attachmentPostResponseDict = json.loads(attachmentPost.content)
            # print('##!!>>', attachmentPostResponseDict['url'])
            receivingAttachment= attachmentPostResponseDict['url']
        
        else:
            receivingAttachment=None

        # checks if user input any received quantity
        # adds the received quantity to latest current stock of part
        # patch received in order record
        # adds a receiving record
        if incomingData['r_received']:
            # add a latest current stock record
            currentGetUrl = f"{request.build_absolute_uri(self.currentEndpoint)}?part__name={incomingData['o_part_name']}"
            currentGet = api_get(url=currentGetUrl, request=request)
            if isinstance(currentGet, HttpResponse):
                return currentGet
            
            currentGetData = currentGet.json()
            currentLatest = currentGetData[-1]
            currentPostUrl = request.build_absolute_uri(self.currentEndpoint)
            currentPostData ={
                'part': incomingData['o_part'],
                'currentStock': int(incomingData['r_received']) + int(currentLatest['currentStock'])
            }

            currentPost = api_post(url=currentPostUrl, request=request, data=json.dumps(currentPostData), post_content_type='json')
            if isinstance(currentPost, HttpResponse):
                return currentPost

            # patch order record
            orderPatchUrl = incomingData['o_url']
            try:
                orderPatchData = {
                    'received':int(incomingData['r_received'])+int(incomingData['o_received']),
                }
            except:
                orderPatchData = {
                    'received':int(incomingData['r_received']),
                }

            # if incomingData['o_received'] != 'None':
                 
            #     orderPatchData = {
            #         'received':int(incomingData['r_received'])+int(incomingData['o_received']),
            #     }
            # orderPatchData = {
            #         'received':int(incomingData['r_received']),
            #     }


            # add record to receiving
            receivingUrl= request.build_absolute_uri(self.receivingEndpoint)
            receivingPostData = {
                    "quantity": int(incomingData['r_received']),
                    "orderItem": incomingData['o_url'],
                    "attachment": receivingAttachment 
                }
            
            receivingPost = api_post(url=receivingUrl, request=request, data= json.dumps(receivingPostData), post_content_type='json')
            if isinstance(receivingPost, HttpResponse):
                return receivingPost
            
            # if received quantity is more than ordered, closes the order
            # print('$$!!>>(received, ordered)', int(incomingData['r_received']), int(incomingData['o_quantity']) )
            if (int(incomingData['r_received']) > int(incomingData['o_quantity'])-int(incomingData['o_received'])) or (int(incomingData['r_received']) == int(incomingData['o_quantity'])-int(incomingData['o_received'])):
                # print('$$!!>>(received, ordered)', int(incomingData['r_received']), int(incomingData['o_quantity']) )
                orderPatchData.update({'status' : "http://127.0.0.1:8000/api/status/2/", 'dateDelivered': incomingData['r_date_received'],})
            
            orderPatch = api_patch(request=request, url=orderPatchUrl, data= json.dumps(orderPatchData), post_content_type='json')
            if isinstance(orderPatch, HttpResponse):
                return orderPatch
                




        return redirect(request.META.get('HTTP_REFERER'))


class ClosePurchaseOrder(LoginRequiredMixin, View):

    # patch order with received=quantity(ordered), status = closed and date delivered !=none (some date)
    # post a current stock of part with latest current stock + order quantity received

    def post(self,request):
        
        incomingData = request.POST
        # print(incomingData)

        orderPatchUrl = incomingData['close_url']
        orderPatchData = {
            'received':incomingData['close_order_quantity'],
            'dateDelivered': incomingData['r_date_delivered'],
            'status' : "http://127.0.0.1:8000/api/status/2/"
        }

        currentEndpoint = request.build_absolute_uri(reverse_lazy('api:currentstock-list'))

        currentGetUrl = f"{currentEndpoint}?part__name={incomingData['close_part_name']}"
        
        currentGet = api_get(url=currentGetUrl, request=request)
        if isinstance(currentGet, HttpResponse):
            return currentGet
        
        currentGetData = currentGet.json()
        currentLatest = currentGetData[-1]
        

        currentPostUrl = currentEndpoint
        currentPostData ={
            'part': incomingData['close_part'],
            'currentStock': int(incomingData['close_order_quantity']) + int(currentLatest['currentStock'])
        }


        orderPatch = api_patch(request=request, url=orderPatchUrl, data= json.dumps(orderPatchData), post_content_type='json')

        if isinstance(orderPatch, HttpResponse):
            return orderPatch

        currentPost = api_post(request=request, url=currentPostUrl, data=json.dumps(currentPostData), post_content_type='json')

        if isinstance(currentPost, HttpResponse):
            return currentPost
        

        return redirect(to= reverse_lazy('frontend:purchasingUpdate', kwargs={'pk': incomingData['redirect_pk'] }))

class OpenPurchaseOrder(LoginRequiredMixin, View):
    template_name='purchasing/openOrder.html'

    def get(self, request,pk):
        orderEndpoint = reverse_lazy('api:order-detail' , kwargs={'pk':pk} )
        orderUrl = request.build_absolute_uri(orderEndpoint)
        orderGet = api_get(url=orderUrl,request=request)

        if isinstance(orderGet, HttpResponse):
            return orderGet
        
        orderData = orderGet.json()
        partUrl = orderData['part']
        partGet =api_get(url=partUrl, request=request)

        if isinstance(partGet, HttpResponse):
            return partGet
        
        partData = partGet.json()

        data = {
            'order': orderData,
            'part': partData
        }



        return render(request=request, template_name=self.template_name, context=data)

    def post(self,request,pk):

        # revert received in order to null/0, revert date delivered to null, revert status of order to open
        # post a new current stock of part with latest current stock - received(which was deleted)

        incomingData = request.POST

        # print(incomingData)

        orderPatchUrl = incomingData['order_url']
        orderPatchData = {
            'received': 0,
            'dateDelivered': None,
            'status' : "http://127.0.0.1:8000/api/status/1/"
        }
        
        currentEndpoint = request.build_absolute_uri(reverse_lazy('api:currentstock-list'))
        currentGetUrl = f"{currentEndpoint}?part__name={incomingData['order_part_name']}"
        currentGet = api_get(url=currentGetUrl, request=request)
        if isinstance(currentGet, HttpResponse):
            return currentGet
        
        currentGetData = currentGet.json()
        currentLatest = currentGetData[-1]
        
        if int(currentLatest['currentStock']) > int(incomingData['order_received']):
            newCurrentStock = int(currentLatest['currentStock']) - int(incomingData['order_received'])
        else: 
            newCurrentStock=0

        currentPostUrl = currentEndpoint
        currentPostData ={
            'part': incomingData['order_part'],
            'currentStock': newCurrentStock
        }


        
        orderPatch = api_patch(request=request, url=orderPatchUrl, data= json.dumps(orderPatchData), post_content_type='json')

        if isinstance(orderPatch, HttpResponse):
            return orderPatch

        currentPost = api_post(request=request, url=currentPostUrl, data=json.dumps(currentPostData), post_content_type='json')

        if isinstance(currentPost, HttpResponse):
            return currentPost



        return redirect(to= reverse_lazy('frontend:purchasingUpdate', kwargs={'pk': incomingData['redirect_pk'] }))


class EditPurchaseOrder(LoginRequiredMixin, View):

    def post(self, request):
        # print(request.POST)
        incomingData= request.POST

        orderPatchUrl = incomingData['e_url']
        orderPatchData={}

        if incomingData['e_ponumber']:
            orderPatchData['poNumber'] = int(incomingData['e_ponumber'])
        
        if incomingData['e_part']:
            orderPatchData['part'] = incomingData['e_part']
        
        if incomingData['e_quantity']:
            orderPatchData['quantity'] = incomingData['e_quantity']

        if incomingData['e_eta']:
            orderPatchData['eta'] = incomingData['e_eta']

        
        orderPatch = api_patch(request=request, url=orderPatchUrl, data= json.dumps(orderPatchData), post_content_type='json')

        if isinstance(orderPatch, HttpResponse):
            return orderPatch
        

        return redirect(request.META.get('HTTP_REFERER'))

class DeletePurchaseOrder(LoginRequiredMixin, View):

    def post(self, request):
        # print(request.POST['d_url'])
        orderDelete= api_delete(request=request,url=request.POST['d_url'])
        if isinstance(orderDelete, HttpResponse):
            return orderDelete

        return redirect(to= reverse_lazy('frontend:purchasingCreate'))