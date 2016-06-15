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

class res_company(osv.osv):
    _inherit = 'res.company'
    _columns = {
        'document_ftp_url': fields.char('Browse Documents', size=128),
        'document_ftp_user': fields.char('FTP Username', required=True),
        'document_ftp_passwd': fields.char('FTP Password', required=True),
    }
    
    _defaults = {
        'document_ftp_url': 'ftp://localhost:8021',
        'document_ftp_user': 'admin',
        'document_ftp_passwd': 'admin'
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: