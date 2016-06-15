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

from openerp import models, fields, api, _

class res_partner(models.Model):
    _inherit = 'res.partner'

    ppp_reference = fields.Char("PPP Reference")

class addsol_hr_expense_line(models.Model):
    _inherit = 'hr.expense.line'
    

    def _code_ref(self):
        query = "select ppp_reference from res_partner where doctor=True and ppp_reference != ''"
        self.env.cr.execute(query)
        return [(row[0], row[0]) for row in self.env.cr.fetchall()]
    
    ppp_reference = fields.Selection(selection=_code_ref, string='PPP Reference')
