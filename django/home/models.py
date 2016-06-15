#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.


class User(models.Model):
    odoo_user_id = models.IntegerField(null=False)
    user_name = models.CharField(max_length=200, null=False)
    odoo_hq_id = models.IntegerField(null=False)

class Group(models.Model):
    odoo_group_id = models.IntegerField(null=False)
    group_name = models.CharField(max_length=200, null=False)

class UserGroup(models.Model):
    odoo_user_id = models.IntegerField(null=False)
    odoo_group_id = models.IntegerField(null=False)
