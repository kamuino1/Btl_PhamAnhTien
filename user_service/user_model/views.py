# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from user_model.models import user_registration
### This function is inserting the data into our table.
def data_insert(fname, lname, email, mobile, password, address):
    user_data = user_registration(fname = fname, lname = lname, email =
    email, mobile = mobile, password = password, address = address)
    user_data.save()
    return 1
### This function will get the data from the front end.
@csrf_exempt
def registration_req(request):
    ### The Following are the input fields.
    if request.method == 'POST':
        if 'application/json' in request.META['CONTENT_TYPE']:
            val1 = json.loads(request.body)
            fname = val1.get("FirstName")
            lname = val1.get("LastName")
            email = val1.get("EmailId")
            mobile = val1.get("MobileNumber")
            password = val1.get("Password")
            cnf_password = val1.get("ConfirmPassword")
            address = val1.get("Address")
            resp = {}
    #### In this if statement, checking that all fields are available.
            if fname and lname and email and mobile and password and cnf_password and address:
            ### This will check that the mobile number is only 10 digits.
                if len(str(mobile)) == 10:
            ### It will check that Password and Confirm Password both arethe same.
                    if password == cnf_password:
            ### After all validation, it will call the data_insert
                        respdata = data_insert(fname, lname, email, mobile,
                            password, address)
        ### If it returns value then will show success.
                        if respdata:
                            resp['status'] = 'Success'
                            resp['status_code'] = '200'
                            resp['message'] = 'User is registered Successfully.'
        ### If it is not returning any value then the show willfail.
                        else:
                            resp['status'] = 'Failed'
                            resp['status_code'] = '400'
                            resp['message'] = 'Unable to register user, Pleasetry again.'
        ### If the Password and Confirm Password is not matched thenit will be through error.
                    else:
                        resp['status'] = 'Failed'
                        resp['status_code'] = '400'
                        resp['message'] = 'Password and Confirm Password should be same.'
        ### If the mobile number is not in 10 digits then it will be through error.
                else:
                    resp['status'] = 'Failed'
                    resp['status_code'] = '400'
                    resp['message'] = 'Mobile Number should be 10 digit.'
        ### If any mandatory field is missing then it will be through 
            else:
                resp['status'] = 'Failed'
                resp['status_code'] = '400'
                resp['message'] = 'All fields are mandatory.'
        else:
            resp['status'] = 'Failed'
            resp['status_code'] = '400'
            resp['message'] = 'All fields are mandatory.'
    else:
        resp['status'] = 'Failed'
        resp['status_code'] = '400'
        resp['message'] = 'All fields are mandatory.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')