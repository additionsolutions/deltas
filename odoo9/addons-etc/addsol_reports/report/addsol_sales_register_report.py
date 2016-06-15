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


class addsol_sales_register_report(models.Model):
    _name = "addsol.sales.register.report"
    _description = ""
    _auto = False
    _order = 'party_name'
    
    party_name = fields.Char("Party Name")
    date_invoice = fields.Date("Invoice Date")
    perticulars = fields.Char("Particulares")
    tally_invoice = fields.Char("Tally Invoice Number")
    salesperson = fields.Char("Salesperson")
    st_name = fields.Char("SalesTeam")
    amount_total = fields.Float("Invoice Total")
    quantity = fields.Integer("Quantity")
    date_due = fields.Date("Due Date")
#    product_id = fields.Many2one('product.product', "Product Id")

    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'addsol_sales_register_report')
        cr.execute("""
            CREATE view addsol_sales_register_report as
                SELECT 
                    min(inv.id) as id,
                    part.name as party_name,
                    inv.date_invoice as date_invoice,
                    inv.comment as perticulars,
                    COALESCE(inv.invoice_tally_no, ' ') as tally_invoice,    
                    res.name as salesperson,
                    COALESCE(st.name, 'Individual') as st_name,
                    sum(inv.amount_total) as amount_total,
                    sum(invl.quantity) as quantity,
                    inv.date_due as date_due
                FROM account_invoice inv
                    JOIN account_invoice_line invl ON invl.invoice_id = inv.id
                    JOIN res_partner part ON part.id = inv.partner_id AND part.active = True
                    LEFT JOIN resource_resource res ON res.user_id = inv.user_id
                    LEFT JOIN account_voucher acnt ON acnt.partner_id = inv.partner_id
                    LEFT JOIN sale_member_rel smr ON smr.member_id = res.user_id
                    LEFT JOIN crm_case_section st ON st.id = smr.section_id 
                WHERE inv.state != 'cancel' 
                GROUP BY
                     part.name,inv.date_invoice,inv.comment,inv.invoice_tally_no, res.name, st.name,inv.date_due
                ORDER BY part.name, inv.date_invoice
        """)
