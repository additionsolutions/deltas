# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015-2016 Addition IT Solutions Pvt. Ltd. (<http://www.aitspl.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
    
class addsol_goals(models.Model):
    _name = 'addsol.goals'
    _rec_name = 'period_id'
    
    #name = fields.Char("Name", required=True)
    #user_id = fields.Many2one('res.users', string="Salesperson", required=True)
    period_id = fields.Many2one('addsol.date.periods', "Period", required=True)
    product_line_ids = fields.One2many('addsol.target.products','target_id', 'Product Lines')
    
    @api.one
    def copy(self, default=None):
        # this is used for create copy or duplicate record
        target_product = []
        for goal_ids in self.browse(self.ids):
            if default is None:
                default = {}
            for line in goal_ids.product_line_ids:
                new_line = line.copy()
                target_product.append(new_line.id)
            default['product_line_ids'] = [(6,0,target_product)]
            res = super(addsol_goals,self).copy(default=default)
        return res
    
class addsol_target_products(models.Model):
    _name = 'addsol.target.products'
    
    target_id = fields.Many2one('addsol.goals')
    product_id = fields.Many2one('product.product', "Product", required=True)
    quantity = fields.Integer("Target Quantity", required=True)


class addsol_date_periods(models.Model):
    _name = 'addsol.date.periods'
    
    name = fields.Char("Name", required=True)
    st_date = fields.Date("Start date", required=True)
    ed_date = fields.Date("End Date", required=True)


class addsol_projection(models.Model):
    _name = 'addsol.projection'
    
    name = fields.Char("Name")
    user_id = fields.Many2one('res.users', "Salesperson")
    period_id = fields.Many2one('addsol.date.periods', "Period")
    projection_line_ids = fields.One2many('addsol.projection.line', 'projection_id', "Projection Lines")
    
    
    @api.one
    @api.constrains('period_id')
    def _check_periodicity_dates(self):
        """ This constraint is used for can not assign same period """
        for periodic_ids in self.browse(self.ids):
            domain =[
                 ('period_id.st_date', '=', periodic_ids.period_id.st_date),
                 ('period_id.ed_date', '=', periodic_ids.period_id.ed_date),
                 ('user_id', '=', periodic_ids.user_id.id),
            ]
            no_repeat_date = self.search_count(domain)
            if no_repeat_date > 1:
                raise Warning(_('Can not assign same period to salesperson'))
        return True
    
    @api.one
    def copy(self, default=None):
        # this is used for create copy or duplicate record
        target_product = []
        for goal_ids in self.browse(self.ids):
            if default is None:
                default = {}
            for line in goal_ids.projection_line_ids:
                new_line = line.copy()
                target_product.append(new_line.id)
            default['user_id'] = 1
            default['projection_line_ids'] = [(6,0,target_product)]
            res = super(addsol_projection,self).copy(default=default)
        return res
    
class addsol_projection_line(models.Model):
    _name = 'addsol.projection.line'
    
    projection_id = fields.Many2one('addsol.projection')
    product_id = fields.Many2one('product.product', "Product")
    projection_qty = fields.Integer("Projection Quantity")
    
    
class addsol_projection_collection(models.Model):
    _name ='addsol.projection.collection'
    
    user_id = fields.Many2one('res.users', "Salesperson")
    period_id = fields.Many2one('addsol.date.periods',"Periods")
    collection_amount = fields.Float("Amount", default=0.0)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
