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


class addsol_outstanding_amount_report(models.Model):
    _name = "addsol.outstanding.amount.report"
    _description = ""
    _auto = False
    
    number = fields.Char("Number")
    tally_invoice = fields.Char("Tally Invoice Number")
    doc_date = fields.Date("Document Date")
    date_due = fields.Date("Due Date")
    residual = fields.Float("Outstanding Amount")
    name = fields.Char("Customer Name")
    days = fields.Integer("Due Days")
    payment_amount = fields.Float("Payment Amount")
    salesperson = fields.Char("Salesperson")
    st_name = fields.Char("SalesTeam")
    invoice_amount = fields.Float("Invoice Amount")
#    product_id = fields.Many2one('product.product', "Product Id")

    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'addsol_outstanding_amount_report')
        cr.execute("""
            CREATE view addsol_outstanding_amount_report as
                 ( SELECT 
                        inv.id as id,
                        inv.number as number,
                        COALESCE(inv.invoice_tally_no, ' ') as tally_invoice,
                        inv.date_invoice as doc_date,
                        inv.date_due as date_due,
                        CASE WHEN inv.type='out_refund'
                             THEN inv.residual * -1
			ELSE inv.residual
			END as residual,
			part.name as name,
                        (current_date - inv.date_invoice) as days,
                        0.0 as payment_amount,
                        res.name as salesperson,
                        COALESCE(st.name, 'Individual') as st_name,
                        CASE WHEN inv.type='out_refund'
                            THEN inv.amount_total * -1
                        ELSE inv.amount_total 
                        END as invoice_amount
                    FROM account_invoice inv
                        JOIN res_partner part ON part.id = inv.partner_id AND part.active = True
                        LEFT JOIN resource_resource res ON res.user_id = inv.user_id
                        LEFT JOIN sale_member_rel smr ON smr.member_id = res.user_id
                        LEFT JOIN crm_case_section st ON st.id = smr.section_id 
                    WHERE inv.state != 'cancel' AND inv.state != 'draft'
                    GROUP BY
                        inv.id, inv.number, inv.date_invoice, inv.date_due, inv.residual, part.name, res.name, st.name, inv.amount_total
                    ORDER BY salesperson, invoice_tally_no, st_name, part.name, inv.date_invoice)
                    UNION ALL
                 ( SELECT 
                        acnt.id as id,
                        acnt.number as number,
                        'Payment'::text as tally_invoice,
                        acnt.date as doc_date,
                        Null as date_due,
                        0.0 as residual,
                        part.name as name,
                        0 as days,
                        acnt.amount as payment_amount,
                        res.name as salesperson,
                        COALESCE(st.name, 'Individual') as st_name,
                        0.0 as invoice_amount
                    FROM account_voucher acnt
                        JOIN res_partner part ON part.id = acnt.partner_id AND part.active = True
                        LEFT JOIN resource_resource res ON res.user_id = part.user_id
                        LEFT JOIN sale_member_rel smr ON smr.member_id = res.user_id
                        LEFT JOIN crm_case_section st ON st.id = smr.section_id 
                    WHERE acnt.state != 'cancel' AND acnt.state != 'draft'
                    GROUP BY
                         acnt.id, part.name, acnt.amount, res.name, st.name
                    ORDER BY part.name)
        """)
