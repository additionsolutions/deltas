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


class party_ledger_report(models.Model):
    _name = "party.ledger.report"
    _description = ""
    _auto = False
    
    party = fields.Char("Party Name")
    mon = fields.Integer("Month")
    opening_balance = fields.Float("Opening Balance")
    invoice_amount = fields.Float("Invoice Amount")
    payment_amount = fields.Float("Payment Amount")
    month_balance = fields.Float("Monthly Balance")
    closing_balance = fields.Float("Closing Balance")

    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'party_ledger_report')
        cr.execute("""
            CREATE view party_ledger_report as
                SELECT part.id, plf.partner_id, part.name as party, plf.mon as mon, plf.invoice_amount, plf.payment_amount, plf.month_balance, plf.closing_balance,
                    (plf.closing_balance - plf.month_balance) as opening_balance
                FROM (SELECT  plg.partner_id as partner_id, plg.mon as mon, plg.invoice_amount, plg.payment_amount, plg.month_balance,

                        (COALESCE( (SELECT sum(pli.month_balance) FROM (SELECT  pl.partner_id as partner_id, pl.mon as mon, 
                            sum(pl.invoice_amount) as invoice_amount, sum(pl.payment_amount) as payment_amount,
                            sum(pl.invoice_amount - pl.payment_amount) as month_balance
                        FROM
                            (SELECT a.id as id, a.partner_id as partner_id, a.date_invoice as doc_date, 
                                CASE WHEN a.type = 'out_invoice'
                                    THEN a.amount_total 
                                     WHEN a.type = 'out_refund'
                                    THEN a.amount_total * -1
                                     ELSE 0
                                END as invoice_amount, 0.0 as payment_amount,
                                EXTRACT (MONTH FROM a.date_invoice) as mon
                            FROM account_invoice a
                            WHERE a.state != 'cancel' AND a.state != 'draft'
                            UNION ALL
                            SELECT acnt.id as id, acnt.partner_id as partner_id, acnt.date as doc_date, 0.0 as invoice_amount,
                                acnt.amount as payment_amount,
                                EXTRACT (MONTH FROM acnt.date) as mon
                            FROM account_voucher acnt WHERE acnt.state != 'draft' AND acnt.state != 'cancel') pl 
                            WHERE pl.partner_id = plg.partner_id AND pl.mon < plg.mon + 1
                            GROUP BY pl.partner_id, pl.mon
                            ) pli),
                            0.0)) as closing_balance
                    FROM (SELECT  pl.partner_id as partner_id, pl.mon as mon, 
                            sum(pl.invoice_amount) as invoice_amount, sum(pl.payment_amount) as payment_amount,
                            sum(pl.invoice_amount - pl.payment_amount) as month_balance
                        FROM
                            (SELECT a.id as id, a.partner_id as partner_id, a.date_invoice as doc_date, 
                                CASE WHEN a.type = 'out_invoice'
                                    THEN a.amount_total 
                                     WHEN a.type = 'out_refund'
                                    THEN a.amount_total * -1
                                     ELSE 0
                                END as invoice_amount, 0.0 as payment_amount,
                                EXTRACT (MONTH FROM a.date_invoice) as mon
                            FROM account_invoice a
                            WHERE a.state != 'cancel' AND a.state != 'draft'
                            UNION ALL
                            SELECT acnt.id as id, acnt.partner_id as partner_id, acnt.date as doc_date, 0.0 as invoice_amount,
                                acnt.amount as payment_amount,
                                EXTRACT (MONTH FROM acnt.date) as mon
                            FROM account_voucher acnt WHERE acnt.state != 'draft' AND acnt.state != 'cancel'
                            UNION ALL
                            SELECT pd.id as id, partn.id as partner_id, pd.date_start as doc_date, 0.0 as invoice_amount,
                                0.0 as payment_amount,
                                EXTRACT (MONTH FROM pd.date_start) as mon
                            FROM res_partner partn
                                JOIN account_period pd ON pd.special=FALSE
                            WHERE partn.customer=True AND partn.active=True
                            ) pl 
                            GROUP BY pl.partner_id, pl.mon
                            ) plg
                    )plf
                    JOIN res_partner part ON part.id = plf.partner_id
                ORDER BY plf.partner_id, plf.mon
        """)
