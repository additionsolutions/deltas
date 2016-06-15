#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from marketing.models import HQ

# Create your models here.


class Employee(models.Model):
    name = models.CharField(max_length=255,null=True)
    login = models.CharField(max_length=200, null=True)
    role = models.CharField(max_length=10,null=True)
    hq = models.ForeignKey(HQ, null=True)
    odoo_parent_id = models.IntegerField(null=True)
    street1 = models.CharField(max_length=255,null=True)
    street2 = models.CharField(max_length=255,null=True)
    city = models.CharField(max_length=255,null=True)
    state_id = models.IntegerField(null=True)
    country_id = models.IntegerField(null=True)
    zip_code = models.CharField(max_length=10, null=True)
    date_of_joining = models.DateField(null=True)
    end_of_probation =  models.DateField(null=True)
    salary = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    da = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    ta = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    notes = models.TextField(null=True)
    gender = models.CharField(max_length=10,null=True) 
    date_of_birth = models.DateField(null=True)
    marital_status = models.CharField(max_length=10,null=True)
    account_no = models.CharField(max_length=15,null=True)
    ifsc_code = models.CharField(max_length=15,null=True)
    bank_id = models.IntegerField(null=True)
    branch = models.CharField(max_length=255,null=True)



#class ppp(models.Model):
#    ppp_date
#    mode = After/Before
#    mr
#    asm
#    hq
#    customer
#    nature = Campaign/ Industry promotion / RoadShow / Counter promotion
#    total_expected_amount
#    period
#    promotional_allowance 
#    allowance_nature = Cash / Gift / other
#    status = Submitted / Approved / Pending / Rejected
#    remark
#    account_remark

#class pppLine(models.Model):
#    product
#    expected_quantity
#    expected_amount
#    

#class pppRecord(model.Model):
#    mr
#    asm
#    pppRecord_date
#    customer
#    amount
#    image
#    aprroved = binary
