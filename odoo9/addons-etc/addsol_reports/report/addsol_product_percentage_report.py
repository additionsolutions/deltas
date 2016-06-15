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

#from openerp.osv import fields, osv
from openerp import models, fields, api, _
from openerp import tools


class product_percentage_report(models.Model):
    _name = "product.percentage.report"
    _description = ""
    _auto = False
    
    product = fields.Char("Product Name")
    quantity = fields.Integer("Quantity")
    month = fields.Char("Month")
    percentage = fields.Float("Percentage")
    #product_id = fields.Many2one('product.product', "Product Id")

    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'product_percentage_report')
        cr.execute("""
                    CREATE view product_percentage_report as
                        SELECT x.id, x.mon as month, x.product as product, x.qnty as quantity,
                            ((x.qnty/sum(x.qnty) OVER (PARTITION BY mon)) *100) as percentage
                        FROM (SELECT 1 as id, EXTRACT(MONTH FROM inv.date_invoice) as mon, invl.name as product,
                                sum(invl.quantity) as qnty
                            FROM account_invoice_line invl
                                JOIN account_invoice inv ON inv.id = invl.id
                                JOIN product_template prd ON prd.id = invl.product_id AND prd.type='product'
                            GROUP BY invl.name, mon
                            ORDER BY mon, qnty DESC
                            ) x
                    """)
