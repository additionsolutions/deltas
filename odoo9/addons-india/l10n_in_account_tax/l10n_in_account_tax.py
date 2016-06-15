# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2013 Tiny SPRL (<http://tiny.be>).
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

import time
from openerp.osv import fields, osv
from openerp.tools.translate import _

TAX_TYPES = [
    ('excise', 'Central Excise'),
    ('cess', 'Cess'),
    ('hedu_cess', 'Higher Education Cess'),
    ('vat', 'VAT'),
    ('add_vat','Additional VAT'),
    ('cst', 'Central Sales Tax'),
    ('service', 'Service Tax'),
    ('tds','Tax Deducted at Source'),
    ('tcs','Tax Collected at Source'),
    ('cform','C Form'),
    ('dform','D Form'),
    ('e1form', 'E1 Form'),
    ('e2form', 'E2 Form'),
    ('fform','F Form'),
    ('hform','H Form'),
    ('iform', 'I Form'),
    ('jform', 'J Form'),
    ('import_duty','Import Duty'),
    ('other', 'Other')
]

class account_tax(osv.osv):
    _inherit = 'account.tax'
    
    _columns = {
        'tax_categ': fields.selection(TAX_TYPES, 'Tax Category'),
        'is_form': fields.boolean('Form ?')
    }
    
    def _unit_compute(self, cr, uid, taxes, price_unit, product=None, partner=None, quantity=0):
        taxes = self._applicable(cr, uid, taxes, price_unit , product, partner)
        res = []
        cur_price_unit = price_unit
        for tax in taxes:
            # we compute the amount for the current tax object and append it to the result
            data = {
                'id':tax.id,
                'name':tax.description and tax.description + " - " + tax.name or tax.name,
                'account_collected_id':tax.account_collected_id.id,
                'account_paid_id':tax.account_paid_id.id,
                'account_analytic_collected_id': tax.account_analytic_collected_id.id,
                'account_analytic_paid_id': tax.account_analytic_paid_id.id,
                'base_code_id': tax.base_code_id.id,
                'ref_base_code_id': tax.ref_base_code_id.id,
                'sequence': tax.sequence,
                'base_sign': tax.base_sign,
                'tax_sign': tax.tax_sign,
                'ref_base_sign': tax.ref_base_sign,
                'ref_tax_sign': tax.ref_tax_sign,
                'price_unit': cur_price_unit,
                'tax_code_id': tax.tax_code_id.id,
                'ref_tax_code_id': tax.ref_tax_code_id.id,
                'include_base_amount': tax.include_base_amount,
                'parent_id':tax.parent_id
            }
            res.append(data)
            if tax.type == 'percent':
                amount = cur_price_unit * tax.amount
                data['amount'] = amount

            elif tax.type == 'fixed':
                data['amount'] = tax.amount
                data['tax_amount'] = quantity
                # data['amount'] = quantity
            elif tax.type == 'code':
                localdict = {'price_unit':cur_price_unit, 'product':product, 'partner':partner}
                exec tax.python_compute in localdict
                amount = localdict['result']
                data['amount'] = amount
            elif tax.type == 'balance':
                data['amount'] = cur_price_unit - reduce(lambda x, y: y.get('amount', 0.0) + x, res, 0.0)
                data['balance'] = cur_price_unit

            amount2 = data.get('amount', 0.0)
            if tax.child_ids:
                if tax.child_depend:
                    latest = res.pop()
                amount = amount2
                child_tax = self._unit_compute(cr, uid, tax.child_ids, amount, product, partner, quantity)
                # Add Parent reference in child dictionary of tax so that we can inlcude tha amount of child ...
                for ctax in child_tax:
                    ctax['parent_tax'] = tax.id
                
                res.extend(child_tax)
                if tax.child_depend:
                    for r in res:
                        for name in ('base', 'ref_base'):
                            if latest[name + '_code_id'] and latest[name + '_sign'] and not r[name + '_code_id']:
                                r[name + '_code_id'] = latest[name + '_code_id']
                                r[name + '_sign'] = latest[name + '_sign']
                                r['price_unit'] = latest['price_unit']
                                latest[name + '_code_id'] = False
                        for name in ('tax', 'ref_tax'):
                            if latest[name + '_code_id'] and latest[name + '_sign'] and not r[name + '_code_id']:
                                r[name + '_code_id'] = latest[name + '_code_id']
                                r[name + '_sign'] = latest[name + '_sign']
                                r['amount'] = data['amount']
                                latest[name + '_code_id'] = False
            
            if tax.include_base_amount:
                cur_price_unit += amount2
                # Check for Child tax addition. If Tax has childrens and they have also set include in base amount we will add it for next tax calculation...
                for r in res:
                    if 'parent_tax' in r and r['parent_tax'] == tax.id:
                        cur_price_unit += r['amount']
        return res

    def onchange_tax_type(self, cr, uid, ids, name, tax_type=False, context=None):
        result = {}
        vals = []
        if tax_type == 'excise' and name:
            base_code_id = self.pool.get('account.tax.code').create(cr,uid,{'name':'Edu.cess 2% on '+name})
            vals = [(0,0, {'name':'Edu.cess 2% on '+name,
                 'tax_type':'cess',
                'sequence':11,
                 'type':'percent',
                 'amount':0.02,
                 'include_base_amount':False,
                 'type_tax_use':'all',
                'base_code_id':base_code_id,
                'tax_code_id':base_code_id,
                }),(0, 0, {'name':'H. Edu.cess 1% on '+name,
                 'tax_type':'hedu_cess',
                'sequence':12,
                 'type':'percent',
                 'amount':0.01,
                 'include_base_amount':False,
                 'type_tax_use':'all',
                'base_code_id':base_code_id,
                'tax_code_id':base_code_id,
                 })]
            base_code_parent_id = self.pool.get('account.tax.code').create(cr,uid,{'name':name})
            result['include_base_amount'] = True
            result['base_code_id'] = base_code_parent_id
            result['tax_code_id'] = base_code_parent_id
        elif tax_type == 'excise' and not name:
            result['tax_categ'] = False
            result['name'] = 'Excise @ ?? %'
        result['child_ids'] = vals
        return {'value': result}

class account_invoice_tax(osv.osv):
    _inherit = 'account.invoice.tax'
    
    _columns = {
        'tax_categ': fields.selection(TAX_TYPES, 'Tax Category'),
        'form_no': fields.char('Form No'),
        'date_iseeu': fields.date('Issue Date'),
        'is_form': fields.boolean('Inter-State Tax')
    }
    
    def compute(self, cr, uid, invoice_id, context=None):
        res = super(account_invoice_tax, self).compute(cr, uid, invoice_id, context=None)
        account_tax_obj = self.pool.get('account.tax')
        for key in res:
            tax_code_id = key[0]
            base_code_id = key[1]
            tax_id = account_tax_obj.search(cr, uid, [('tax_code_id', '=', tax_code_id), ('base_code_id', '=', base_code_id)], context=context)
            for id in tax_id:
                tax = account_tax_obj.browse(cr, uid, id, context=context)
                res[key]['tax_categ'] = tax.tax_categ
                res[key]['is_form'] = tax.is_form
        return res

account_invoice_tax()

class res_partner(osv.osv):
    
    _inherit = "res.partner"
    
    _columns = {
        'tin_no': fields.char('TIN Number', size=32, help="Tax Identification Number"),
        'tin_date': fields.date('TIN Number Issue Date', help="Tax Identification Number Date of Company"),
        
        'cst_no': fields.char('CST Number', size=32, help='Central Sales Tax Number of Company'),
        'cst_date': fields.date('CST Number Issue Date', help='Central Sales Tax Date of Company'),
        
        'vat_no' : fields.char('VAT Number', size=32, help="Value Added Tax Number"),
        'vat_date': fields.date('VAT Number Issue Date', help='VAT Number Issue Date'),
        
        'excise_no': fields.char('Excise Control Code', size=32, help="Excise Control Code"),
        'excise_date': fields.date('Excise Code Issue Date',  help="Excise Code Issue Date"),
        
        'service_no' : fields.char('ST Number', size=32, help="Service Tax Number"),
        'service_date' : fields.date('ST Number Issue Date', help="Issue Date of Service Tax Number"),
        
        'pan_no' : fields.char('PAN', size=32, help="Permanent Account Number")
    }
res_partner()

class res_company(osv.osv):
    
    _inherit = 'res.company'
    
    _columns = {
        'range': fields.char('Range', size=64),
        'division': fields.char('Division', size=64),
        'commissionerate': fields.char('Commissionerate', size=64),
        'tariff_rate': fields.integer('Tariff Rate'),
        'tan_no' : fields.char('Tax Deduction Account Number', size=32, help="Tax Deduction Account Number"),
    }
res_company()

class account_invoice_type(osv.osv):
    
    _name = 'account.invoice.type'
    _description = "Invoice Type"
    
    _columns = {
        'name': fields.char('Name', size=64),
        'journal_id': fields.many2one('account.journal', 'Account Journal'),
        'type': fields.selection([
            ('out_invoice','Customer Invoice'),
            ('in_invoice','Supplier Invoice'),
            ('out_refund','Customer Refund'),
            ('in_refund','Supplier Refund'),
            ],'Type', select=True),
        'report': fields.many2one('ir.actions.report.xml', 'Report', domain=[('model','=','account.invoice')])
    }
res_company()

class account_invoice(osv.osv):
    
    _inherit = 'account.invoice'
    
    _columns = {
        'invoice_type_id': fields.many2one('account.invoice.type', 'Invoice')
    }
    
    def onchange_invoice_type(self, cr, uid, ids, invoice_type_id, context=None):
        res = {}
        if invoice_type_id:
            type_pool = self.pool.get('account.invoice.type')
            type = type_pool.browse(cr, uid, invoice_type_id)
            if type.journal_id:
                res.update({'journal_id':type.journal_id.id})
            else:
                raise osv.except_osv(_('Warning!'),_('Please define Journal on %s Invoice type' % (type.name)))
        
        return {'value':res}

    def invoice_print(self, cr, uid, ids, context=None):
        report = super(account_invoice, self).invoice_print(cr, uid, ids, context)
        
        invoice = self.browse(cr, uid, ids[0])
        if invoice.invoice_type_id and invoice.invoice_type_id.report:
            report_new = {
                'type': invoice.invoice_type_id.report.type,
                'report_name': invoice.invoice_type_id.report.report_name
            }
            report.update(report_new)
            
        return report

res_company()

class product_category(osv.Model):
    _inherit = 'product.category'

    _columns = {
        'hsn': fields.char('HSN Classification', size=256),
        'chapter_no': fields.char('Ex-Chapeter No.', size=256),
    }

product_category()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
