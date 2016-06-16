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

import threading
import openerp
from openerp import tools, api
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp
from datetime import date

class addsol_hr(models.Model):
	_inherit = 'hr.employee'
	
	date_join = fields.Date("With Effect From")
	company_name = fields.Selection([('Deltas_Pharma','Deltas Pharma'), ('Deltas Pharma Pvt. Ltd.','Deltas Pharma Pvt. Ltd.')], 'Company')
	birth_state_id = fields.Many2one('res.country.state', "State Of Birth", ondelete='restrict')
	birth_country_id = fields.Many2one('res.country', "Country", ondelete='restrict')
	religion = fields.Char("Religion")
	nationality = fields.Char("Nationality")
	marraige_date = fields.Date("Date of Marraige")
	mother_tongue = fields.Char("Mother Tongue")
	mobile_no = fields.Char("Mobile")
	height = fields.Integer("Height")
	weight = fields.Integer("Weight")
	bloodgroup = fields.Char("Blood Group")
	joining_flag = fields.Boolean("Joining", default=False)
	addsol_education_ids = fields.One2many('addsol.employee.education', 'employee_id')
	addsol_previous_details_ids = fields.One2many('addsol.previous.employer.details', 'employee_id')
	addsol_employee_family_details_ids = fields.One2many('addsol.employee.family.details', 'employee_id')
	
	@api.multi
	def onchange_state(self, birth_state_id):
		if birth_state_id:
			state = self.env['res.country.state'].browse(birth_state_id)
			return {'value': {'birth_country_id': state.country_id.id}}
		return {'value': {}}
		
		
class addsol_employee_education(models.Model):
	_name = 'addsol.employee.education'
	
	employee_id = fields.Many2one('hr.employee')
	college_name = fields.Char("Institution/College/School")
	degree = fields.Char("Degree/Diploma")
	from_date = fields.Date("From")
	to_date = fields.Date("To")
	university_name = fields.Char("University Name")
	percentage = fields.Char("Percentage/Grade")
	branch = fields.Char("Branch")
	
class addsol_previous_employer_details(models.Model):
	_name = 'addsol.previous.employer.details'
	
	employee_id = fields.Many2one('hr.employee')
	from_date = fields.Date("From")
	to_date = fields.Date("To")
	company_name = fields.Char("Company Name")
	city = fields.Char("City")
	industry = fields.Char("Industry/Business")
	job_title = fields.Char("Job Title")
	responsibilities = fields.Text("Responsibilities")
	previous_salary = fields.Float("Previous Salary Per Annum")
	
class addsol_employee_family_details(models.Model):
	_name = 'addsol.employee.family.details'
	
	employee_id = fields.Many2one('hr.employee')
	name = fields.Char("Name")
	firstName = fields.Char("First Name")
	middleName = fields.Char("Middle Name")
	lastName = fields.Char("Last Name")
	relationship = fields.Char("Relationship")
	dob = fields.Date("Date of Birth")
	occupation = fields.Char("Occupation")
	personal_emailid = fields.Char("EmailId")

#class addsol_res_user(models.Model):
#	_inherit = 'res.users'

#	invitation = fields.Boolean("Invitation", default=False)
	
