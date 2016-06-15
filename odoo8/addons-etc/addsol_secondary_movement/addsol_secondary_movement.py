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
import openerp.addons.decimal_precision as dp
from datetime import date

class secondary_movement(models.Model):
    _name = 'secondary.movement'
    _rec_name = 'movement_date'
    
    partner_id = fields.Many2one('res.partner', "Superstockist", required=True)
    movement_date = fields.Date("Date", default=date.today())
    stockist_partner_id = fields.Many2one('res.partner', "Stockist")
    sale_amount = fields.Float("Sale Amount", defualt=0.0)
    collection_amount = fields.Float("Collection Amount", default=0.0)
    secondary_movement_line_ids = fields.One2many('secondary.movement.line', 'secondary_movement_id', "Stockistwise Movement")
    
    
class secondary_movement_line(models.Model):
    _name = 'secondary.movement.line'
    
    @api.depends('quantity','unit_price')
    def _compute_amount(self):
        self.amount = self.quantity * self.unit_price
        return self.amount
    
    secondary_movement_id = fields.Many2one('secondary.movement')
    product_id = fields.Many2one('product.product', "Product")
    quantity = fields.Integer("Quantity", default=0)
    unit_price = fields.Float("Unit Price", digits= dp.get_precision('Product Price'))
    amount = fields.Float("Amount", digits= dp.get_precision('Account'), store=True, readonly=True, compute='_compute_amount')