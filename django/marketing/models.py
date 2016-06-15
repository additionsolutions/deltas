#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.

class HQ(models.Model):
    odoo_hq_id = models.IntegerField(null=False)
    hq_name = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.hq_name


class Product(models.Model):
    odoo_product_id = models.IntegerField(null=False)
    product_name = models.CharField(max_length=200, null=False)
    product_price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.product_name


class SalesTeam(models.Model):
    odoo_mr_id = models.IntegerField(null=False)
    mr_name = models.CharField(max_length=200, null=False)
    odoo_asm_id = models.IntegerField(null=False)
    asm_name = models.CharField(max_length=200, null=False)
    odoo_rsm_id = models.IntegerField(null=True)
    rsm_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.mr_name + '-' + self.asm_name + '-' + self.rsm_name


class Doctor(models.Model):
    odoo_doctor_id = models.IntegerField(null=False)
    doctor_name = models.CharField(max_length=200, null=False)
    street1 = models.CharField(max_length=200, null=True)
    street2 = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zip = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    mobile = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=40, null=True)
    odoo_hq_id = models.IntegerField(null=False)
    ppp_reference = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.doctor_name


class Chemist(models.Model):
    odoo_chemist_id = models.IntegerField(null=False)
    chemist_name = models.CharField(max_length=200, null=False)
    street1 = models.CharField(max_length=200, null=True)
    street2 = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zip = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    mobile = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=40, null=True)
    odoo_hq_id = models.IntegerField(null=False)
    odoo_doctor_id = models.IntegerField(null=True)
    prefered = models.BooleanField

    def __str__(self):
        return self.chemist_name


class Stockist(models.Model):
    odoo_stockist_id = models.IntegerField(null=False)
    stockist_name = models.CharField(max_length=200, null=False)
    street1 = models.CharField(max_length=200, null=True)
    street2 = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zip = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    mobile = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=40, null=True)

    def __str__(self):
        return self.stockist_name


class StockistLine(models.Model):
    odoo_stockist_id = models.IntegerField(null=False)
    odoo_hq_id = models.IntegerField(null=False)

    def __str__(self):
        return self.odoo_hq_id


class PPP(models.Model):
    AFTER = 'AR'
    BEFORE = 'BE'
    MODE = (
        (AFTER, 'After'),
        (BEFORE, 'Before'),
    )
    mode = models.CharField(max_length=2,
                                      choices=MODE,
                                      default=AFTER)
    SUBMITTED = 'DR'
    APPROVED = 'AP'
    REJECTED = 'RJ'
    STATUS = (
        (SUBMITTED, 'Submitted'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    )
    status = models.CharField(max_length=2,
                                      choices=STATUS,
                                      default=SUBMITTED)
    ppp_date = models.DateTimeField('PPP date')
    odoo_asm_id = models.IntegerField(null=False)
    odoo_mr_id = models.IntegerField(null=False)
    odoo_hq_id = models.IntegerField(null=False)
    odoo_doctor_id = models.IntegerField(null=False)
    total_amount = models.DecimalField(max_digits=7, decimal_places=2)
    promotional_activity = models.CharField(max_length=200, null=True)
    period = models.CharField(max_length=200, null=True)
    promotional_expenses = models.CharField(max_length=200, null=True)
    disbursement_nature = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.ppp_date 


class PPPLine(models.Model):
    ppp = models.ForeignKey(PPP, on_delete=models.CASCADE)
    odoo_product_id = models.IntegerField(null=False)
    quantity = models.DecimalField(max_digits=7, decimal_places=2)
    rate = models.DecimalField(max_digits=7, decimal_places=2)
    amount = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.odoo_product_id
