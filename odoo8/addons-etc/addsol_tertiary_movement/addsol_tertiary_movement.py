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

class addsol_tertiary_movement(models.Model):
    _name = 'addsol.tertiary.movement'
    _rec_name = 'movement_date'
    
    partner_id = fields.Many2one('res.partner', "Stockist", required=True)
    movement_date = fields.Date("Date", default=date.today())
    tertiary_movement_line_ids = fields.One2many('addsol.tertiary.movement.line', 'tertiary_movement_id')
    
    
class addsol_tertiary_movement_line(models.Model):
    _name = 'addsol.tertiary.movement.line'
    
    tertiary_movement_id = fields.Many2one('addsol.tertiary.movement')
    chemist_partner_id = fields.Many2one('res.partner', "Chemist")
    amount = fields.Float("Amount", default=0.00)
    
    