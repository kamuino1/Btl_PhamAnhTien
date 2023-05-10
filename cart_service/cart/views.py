from django.http import HttpResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Cart
from django.db.models import F

def store_data(uname, date, product, quantity):
    user_data = Cart(username = uname,date_added= date, product_id = product, quantity= quantity)
    user_data.save()
    return 1

def cart_data(uname):
    cart = Cart.objects.all().filter(username = uname)
    data = []
    for data in cart.values():
        return data

def cart_data_by_product(uname, product_id):
    cart = Cart.objects.filter(username = uname, product_id = product_id)
    return cart

def cart_data_by_id(id):
    cart = Cart.objects.filter(id = id)
    for data in cart.values():
        return data

@csrf_exempt
def add_product_to_cart(request):
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)
            uname = val1.get('username')
            date = val1.get('date')
            product_id = val1.get('productid')
            quantity = val1.get('quantity')
            respdata = cart_data_by_product(uname=uname, product_id=product_id)
            resp = {}
            if uname and date and product_id and quantity:
                if respdata:
                    respdata.update(quantity = Cart.objects.get(username = uname, product_id = product_id).quantity + int(quantity))
                    resp['status'] = 'Success'
                    resp['status_code'] = '200'
                    resp['message'] = 'Add success'
                else:
                    respdata = store_data(uname, date, product_id, quantity)
                    if respdata:
                        resp['status'] = 'Success'
                        resp['status_code'] = '200'
                        resp['message'] = 'Add success'
                    else:
                        resp['status'] = 'Failed'
                        resp['status_code'] = '400'
                        resp['message'] = 'User Not Found.'
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'Fields is mandatory.'
        else:
            resp['status'] = 'Failed'
            resp['status_code'] = '400'
            resp['message'] = 'Request type is not matched.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')

@csrf_exempt
def get_cart(request):
    if request.method == 'GET':
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)
            uname = val1.get('username')
            resp = {}
            if uname:
                cart = Cart.objects.filter(username=uname)
                cart_list = []
                for data in cart.values():
                    dict1 = {}
                    dict1['ID'] = data.get('id', '')
                    dict1['Username'] = data.get('username', '')
                    dict1['Date'] = data.get('date_added', '').strftime("%d.%m.%Y"),
                    dict1['Product ID'] = data.get('product_id', '')
                    dict1['Quantity'] = data.get('quantity', '')
                    cart_list.append(dict1)
                if cart_list:
                    resp['status'] = 'Success'
                    resp['status_code'] = '200'
                    resp['data'] = cart_list
                else:
                    resp['status'] = 'Failed'
                    resp['status_code'] = '400'
                    resp['message'] = 'Shopping cart clear'
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'Fields are mandatory.'
        else:
            resp['status'] = 'Failed'
            resp['status_code'] = '400'
            resp['message'] = 'Request type is not matched.'
    else:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'Request type is not matched.'
    return HttpResponse(json.dumps(resp), content_type='application/json')

@csrf_exempt
def remove_cart(request):
    if request.method == 'DELETE':
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)
            uname = val1.get('username')
            product_id = val1.get('product_id')
            resp = {}
            if uname and product_id:
                respdata = cart_data_by_product(uname=uname, product_id=product_id)
                resp = {}
                if respdata:
                    respdata.delete()
                    resp['status'] = 'Success'
                    resp['status_code'] = '200'
                    resp['message'] = 'Remove success'                  
                else:
                    resp['status'] = 'Failed'
                    resp['status_code'] = '400'
                    resp['message'] = 'User Not Found.'
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'Fields is mandatory.'
        else:
            resp['status'] = 'Failed'
            resp['status_code'] = '400'
            resp['message'] = 'Request type is not matched.'
    else:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'Request type is not matched.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')