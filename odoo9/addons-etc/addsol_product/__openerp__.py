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
    'name': "addsol_product",

    'summary': """
        Product modification to include multiple synonyms and QA checking flag""",

    'description': """
        Addition IT Solutions Pvt. Ltd.
		=================================
		Contact :
			* website : www.aitspl.com
			* email   : info@aitspl.com
			
		Producr modification Module:
		----------------------------
		* Add new fields for synonyms : Name 1, Name 2, Name 3 and CAS#
		* Add QA required flag
		* Add search functionality for newly added fields
    """,

    'author': "Addition IT Solutions Pvt. Ltd.",
    'website': "http://www.aitspl.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'AddSol mods',
    'version': '0.1',
	# 'images' : ['images/addsol.png'],
	
    # any module necessary for this one to work correctly
    'depends': ['product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
		'views/addsol_product_view.xml',
		#'views/product.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}