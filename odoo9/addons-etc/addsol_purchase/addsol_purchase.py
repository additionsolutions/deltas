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
from openerp.osv import fields, osv


class addsol_purchase(osv.Model):
	
	_inherit = "purchase.order"
	_columns = {
				 'excise_control_code':fields.related('partner_id','excise_no',type='char',string='Excise Control Code',size=64),
				 'tin_no': fields.related('partner_id','tin_no',type='char',string='TIN No',size=64),
				 'dppl_tin':fields.selection([('27171018888','27171018888'),('05015331554','05015331554')],'DPPL TIN', required=True),
				 'order_ref_no':fields.char('Order Reference No',Size=64),
				 'product_id':fields.many2one('product.product', 'Finished Product Name'),
				 'price_basis':fields.selection([('Ex Factory','Ex Factory'),('FOR','FOR'),('FOB','FOB'),('Door Delivery','Door Delivery'),('CIF','CIF'),('CIP','CIP')],'Price Basis'),
				 'transport_doc_no':fields.char('Transport Doc. No.',size=64),
	}
	
       
	
class addsol_purchase_order_line(osv.osv):
    
    _inherit = "purchase.order.line"
    _columns = {
        'detail': fields.char('Detail',size=64),   
    }
	
	
class res_company(osv.osv):
    
    _inherit = 'res.company'
    _columns = {
        'range': fields.char('Range', size=64),
        'division': fields.char('Division', size=64),
        'commissionerate': fields.char('Commissionerate', size=64),
        'tariff_rate': fields.integer('Tariff Rate'),
        'tan_no' : fields.char('Tax Deduction Account Number', size=32, help="Tax Deduction Account Number"),
    }

	
class product_category(osv.Model):

    _inherit = 'product.category'
    _columns = {
        'hsn': fields.char('HSN Classification', size=256),
        'chapter_no': fields.char('Ex-Chapeter No.', size=256),
    }
	
	
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
        
        'service_no' : fields.char('Service Tax Number', size=32, help="Service Tax Number"),
        'service_date' : fields.date('ST Number Issue Date', help="Issue Date of Service Tax Number"),
        
        'pan_no' : fields.char('PAN', size=32, help="Permanent Account Number"),
    }