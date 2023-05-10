from django.http import HttpResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from .models import comment
from django.db.models import F

def store_data(uname, date, product, content):
    comment_data = comment(username = uname,date_added= date, product_id = product, content= content)
    comment_data.save()
    return 1

def comment_data(product):
    Comment = comment.objects.filter(product_id = product)
    data = []
    for data in Comment.values():
        return data

def comment_data_by_product(uname, product_id):
    Comment = comment.objects.filter(username = uname, product_id = product_id)
    return Comment

def comment_data_by_id(id):
    Comment = comment.objects.filter(id = id)
    for data in Comment.values():
        return data

@csrf_exempt
def add_comment(request):
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)
            uname = val1.get('username')
            date = val1.get('date')
            product_id = val1.get('productid')
            content = val1.get('content')
            respdata = comment_data_by_product(uname=uname, product_id=product_id)
            resp = {}
            if uname and date and product_id and content:
                if respdata:
                    respdata.update(content = comment.objects.get(username = uname, product_id = product_id).content + content)
                    resp['status'] = 'Success'
                    resp['status_code'] = '200'
                    resp['message'] = 'Add success'
                else:
                    respdata = store_data(uname, date, product_id, content)
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
def get_comment(request):
    if request.method == 'GET':
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)
            product = val1.get('product_id')
            resp = {}
            if product:
                Comment = comment.objects.filter(product_id=product)
                comment_list = []
                for data in Comment.values():
                    dict1 = {}
                    dict1['ID'] = data.get('id', '')
                    dict1['Username'] = data.get('username', '')
                    dict1['Date'] = data.get('date_added', '').strftime("%d.%m.%Y"),
                    dict1['Product ID'] = data.get('product_id', '')
                    dict1['Content'] = data.get('content', '')
                    comment_list.append(dict1)
                if comment_list:
                    resp['status'] = 'Success'
                    resp['status_code'] = '200'
                    resp['data'] = comment_list
                else:
                    resp['status'] = 'Failed'
                    resp['status_code'] = '400'
                    resp['message'] = 'User not found'
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
def remove_comment(request):
    if request.method == 'DELETE':
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)
            id = val1.get('id')
            resp = {}
            if id:
                respdata = comment.objects.filter(id = id)
                if respdata:
                    resp['status'] = 'Success'
                    resp['status_code'] = '200'
                    resp['message'] = 'Remove success'
                    respdata.delete()
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