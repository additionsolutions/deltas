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
    'name': 'Report Customization - Addsol',
    'version': '1.0',
    'author': 'Addition IT Solutions Pvt. Ltd.',
    'category': 'Accounting & Finance',
    'summary': 'Report Customization for Accounting',
    'website': 'https://www.aitspl.com',
    'description': """
Report Customization
======================
	This module add Partner in filter list.
	You can select one or many partners for the report.
    
Contact:
    * website: www.aitspl.com
    * email: info@aitspl.com    
    
""",
    'images': [],
    'depends': ['account'],
    'data': [
        'wizard/account_report_partner_ledger_view.xml',
        'views/report_partnerledger.xml',
        'views/report_partnerledgerother.xml',
     ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: