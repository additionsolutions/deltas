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
    'name' : 'Addsol Invoice Tally',
    'summary': 'Add Tally invoice number',
    'description' : """
Addition IT Solutions Pvt. Ltd.
=================================
    Contact:
    * website: www.aitspl.com
    * email: info@aitspl.com
    
Features:
---------
    * This is to create link between Tally invoice & Odoo invoice
     
""",

    'author' : 'Addition IT Solutions Pvt. Ltd.',
    
    'category' : 'Addsol mods',
    'version' : '1.0',
    
    'depends' : ['account'],
    
    'data': [
        #'security/ir.model.access.csv',
        #'templates.xml',
        'views/addsol_invoice_tally_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
