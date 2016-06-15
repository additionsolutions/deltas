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
{
    'name' : 'AddSol Reports',
    'summary': 'Reports Customization',
    'description' : """
Addition IT Solutions Pvt. Ltd.
=================================
    Contact:
    * website: www.aitspl.com
    * email: info@aitspl.com
    
Features:
---------
    * Additional reports 
     
""",

    'author' : 'Addition IT Solutions Pvt. Ltd.',
    
    'category' : 'Addsol mods',
    'version' : '1.0',
    
    'depends' : ['account','crm'],
    
    'data': [
        #'templates.xml',
        'security/ir.model.access.csv',
        'report/addsol_top_product_report_view.xml',
        'report/addsol_product_percentage_report_view.xml',
	'report/addsol_outstanding_amount_report_view.xml',
        'report/addsol_party_ledger_report_view.xml',
        'report/addsol_goals_vs_actuals_report_view.xml',
        'report/addsol_profitability_report_view.xml',
        'report/addsol_MOA_invoice_report_view.xml',
        'addsol_sales_register_report.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
