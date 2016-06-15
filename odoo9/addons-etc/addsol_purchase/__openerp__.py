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
    'name': 'Addsol Purchase',
    'version': '1.0',
    'category': 'Purchase Management',
    'description': """
Addition IT Solutions Pvt. Ltd.
====================================
Contact :
    * website : www.aitspl.com
    * email   : info@aitspl.com
	
Purchase order Module:
----------------------------
* Add new fields such as excise no. and tin no. of supplier
* Add tin no of parent company
* Add detail field for description or specification of product in purchase order line   

    """,
    'author': 'Addition IT Solutions Pvt. Ltd. ',
    'website': 'http://www.aitspl.com',
    'images' : ['images/addsol.png'],
    'depends': ['purchase'],
    'data': ['addsol_purchase_view.xml',
             'views/report_addsol_purchase.xml',
             'addsol_purchase_report.xml'],
    'test': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
