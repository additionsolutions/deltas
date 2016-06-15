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
from datetime import date,timedelta
import openerp.addons.decimal_precision as dp


class mr_tour_plan(models.Model):
    _name = 'mr.tour.plan'
    description = "MR Tour Information"
   
         
    name = fields.Char("Name")
    employee_id = fields.Many2one('hr.employee', "MR")
    tour_date = fields.Date("Date")
    tour_date_to = fields.Date("Date To")
    is_approved = fields.Boolean()
    approved_date = fields.Datetime()
    notes = fields.Text("Notes")
    
    @api.cr_uid_ids_context
    def _employee_get(self, cr, uid, context=None):
        emp_id = context.get('default_employee_id', False)
        if emp_id:
            return emp_id
        ids = self.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)], context=context)
        if ids:
            return ids[0]
        return False
     
    _defaults = {
     'employee_id' : _employee_get
     }

class mr_tour_plan_doctor(models.Model):
    _name = 'mr.tour.plan.doctor'
         
    tour_id = fields.Many2one('mr.tour.plan', "Tour Plan")
    dr_partner_id = fields.Many2one('res.partner', "Doctor")
    plan_doctor_work_with_line_ids = fields.One2many('plan.doctor.work.with.line', 'plan_doctor_id', "Work with whom")
    plan_doctor_product_line_ids = fields.One2many('plan.doctor.product.line', 'plan_doctor_id', "Plan Product")
    plan_doctor_samples_line_ids = fields.One2many('plan.doctor.samples.line', 'plan_doctor_id', "Plan Samples")
    plan_doctor_promotional_line_ids = fields.One2many('plan.doctor.promotional.line', 'plan_doctor_id', "Plan Promotional")
    notes = fields.Text("Notes")
    
class plan_doctor_work_with_line(models.Model):
    _name = 'plan.doctor.work.with.line'
    
    plan_doctor_id = fields.Many2one('mr.tour.plan.doctor')
    employee_id = fields.Many2one('hr.employee', "Work with whom")
    
class plan_doctor_product_line(models.Model):
    _name = 'plan.doctor.product.line'
    
    plan_doctor_id = fields.Many2one('mr.tour.plan.doctor')
    product_id = fields.Many2one('product.product', "Product")
    
class plan_doctor_samples_line(models.Model):
    _name = 'plan.doctor.samples.line'
    
    plan_doctor_id = fields.Many2one('mr.tour.plan.doctor')
    product_id = fields.Many2one('product.product', "Sample Product")
    sample_qty = fields.Integer("Quantity", default=0)

class plan_doctor_promotional_line(models.Model):
    _name = 'plan.doctor.promotional.line'
    
    plan_doctor_id = fields.Many2one('mr.tour.plan.doctor')
    product_id = fields.Many2one('product.product', "Promotional Product")
    promotional_qty = fields.Integer("Quantity", default=0)

class mr_tour_plan_chemist(models.Model):
    _name = 'mr.tour.plan.chemist'
    
    tour_id = fields.Many2one('mr.tour.plan', "Tour Plan")
    chemist_partner_id = fields.Many2one('res.partner', "Chemist")
    plan_chemist_work_with_line_ids = fields.One2many('plan.chemist.work.with.line', 'plan_chemist_id', "Work with whom")
    notes = fields.Text("Notes")

    
class plan_chemist_work_with_line(models.Model):
    _name = 'plan.chemist.work.with.line'
      
    plan_chemist_id = fields.Many2one('mr.tour.plan.chemist', string='Chemist Reference')
    employee_id = fields.Many2one('hr.employee', "Work with whom")
     
class mr_tour_plan_stockist(models.Model):
    _name = 'mr.tour.plan.stockist'
    
    tour_id = fields.Many2one('mr.tour.plan', "Tour Plan")
    stockist_partner_id = fields.Many2one('res.partner', "Stockist")
    plan_stockist_work_with_line_ids = fields.One2many('plan.stockist.work.with.line', 'plan_stockist_id', "Work with whom")
    notes = fields.Text("Notes")

      
class plan_stockist_work_with_line(models.Model):
    _name = 'plan.stockist.work.with.line'
      
    plan_stockist_id = fields.Many2one('mr.tour.plan.stockist', string='Chemist Reference')
    employee_id = fields.Many2one('hr.employee', "Work with whom")


class mr_daily_doctor_call(models.Model): 
    _name = 'mr.daily.doctor.call'
    description = "Daily Call of Doctor"
    _rec_name = 'call_date'
    
    employee_id = fields.Many2one('hr.employee', "MR")
    call_date = fields.Date("Date", default=date.today())
    dr_partner_id = fields.Many2one('res.partner', "Doctor")
    call_product_line_ids = fields.One2many('mr.daily.doctor.call.line', 'doctor_call_id', "Product")
    remark = fields.Text("Remark")
    unplanned_doctor = fields.Boolean("Unplanned Doctor", help="Check this box if doctor is not in planned list")
    telephonic_flag = fields.Boolean("Telephonic Call")
    reasons = fields.Selection([('due to rain', 'Due To rain'),('personal reason', 'Personal Reason')], 'Select Reason')
    work_with_ids = fields.Many2many('hr.employee', 'mr_daily_doctor_work_with', 'mr_daily_doctor_work_id', 'employee_id', string='Work With Whom')
    
    @api.cr_uid_ids_context
    def _employee_get(self, cr, uid, context=None):
        emp_id = context.get('default_employee_id', False)
        if emp_id:
            return emp_id
        ids = self.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)], context=context)
        if ids:
            return ids[0]
        return False
    
    _defaults = {
     'employee_id' : _employee_get
     }
    
    
class mr_daily_doctor_call_line(models.Model):
    _name = 'mr.daily.doctor.call.line'
    
    doctor_call_id = fields.Many2one('mr.daily.doctor.call')
    product_id = fields.Many2one('product.product', "Sample Product")
    quantity = fields.Integer("Sample Product Quantity", default=0)
    chemist_qty = fields.Integer("Chemist Quantity", default=0, readonly=True)
    stockist_qty = fields.Integer("Stockist Quantity", default=0, readonly=True)
    scheme_product_id = fields.Many2one('scheme.product', "Scheme")
    
    
class mr_daily_chemist_call(models.Model):
    _name = 'mr.daily.chemist.call'
    description = "Daily Call of Chemist"
     
    employee_id = fields.Many2one('hr.employee', "MR")
    call_date = fields.Date("Date", default=date.today())
    partner_id = fields.Many2one('res.partner', "Chemist")
    inventory_product_line_ids = fields.One2many('mr.daily.chemist.inventory', 'chemist_call_inv_id', "Inventory Product", states={'draft': [('readonly', False)]} , readonly=True)
    order_product_line_ids = fields.One2many('mr.daily.chemist.order', 'chemist_call_ord_id', "Order Product", states={'draft': [('readonly', False)]} , readonly=True)
    state = fields.Selection([('draft', 'To Submit'),('confirm', 'Confirmed')], 'Status', readonly=True)
    chemist_work_with_ids = fields.Many2many('hr.employee', 'mr_daily_chemist_work_with', 'mr_daily_chemist_work_id', 'employee_id', string='Work With Whom')
    remark = fields.Text("Remark")
    telephonic_flag = fields.Boolean("Telephonic Call")
    reasons = fields.Selection([('due to rain', 'Due To rain'),('personal reason', 'Personal Reason')], 'Select Reason')
    
    @api.cr_uid_ids_context
    def _employee_get(self, cr, uid, context=None):
        emp_id = context.get('default_employee_id', False)
        if emp_id:
            return emp_id
        ids = self.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)], context=context)
        if ids:
            return ids[0]
        return False
     
    _defaults = {
     'employee_id' : _employee_get,
      'state': 'draft'
     }
     
    @api.one
    def plan_send(self):
        self.write({'state': 'confirm'})
        return True
         
     
class mr_daily_chemist_inventory(models.Model):
    _name = 'mr.daily.chemist.inventory'
     
    chemist_call_inv_id = fields.Many2one('mr.daily.chemist.call')
    product_id = fields.Many2one('product.product', "Product")
    inv_prod_quantity = fields.Integer("Quantity", default=0)
    state = fields.Selection([('damaged','Damaged'),('expire','Expire'),('normal','Normal'),('return','Return')])
     
    _defaults = {
     'state' : 'normal'
     }
     
class mr_daily_chemist_order(models.Model):
    _name = 'mr.daily.chemist.order'
     
    chemist_call_ord_id = fields.Many2one('mr.daily.chemist.call')
    product_id = fields.Many2one('product.product', "Product")
    ord_prod_quantity = fields.Integer("Quantity", default=0)
    last_mnth_qty = fields.Integer("Last Month Quantity", default=0, readonly=True)
    till_date_quantity = fields.Integer("Till Date quantity", default=0, readonly=True)
    stockist_qty = fields.Integer("Stockist Quantity", default=0, readonly=True)
    scheme_product_id = fields.Many2one('scheme.product', "Scheme")

class weekly_stockist_call(models.Model):
    _name = 'weekly.stockist.call'
    description = "Weekly call of stockist"
     
    employee_id = fields.Many2one('hr.employee', "MR")
    call_date = fields.Date("Date", default=date.today())
    partner_id = fields.Many2one('res.partner', "Stockist")
    from_date = fields.Date("From Date", default=date.today())
    to_date = fields.Date("To Date", default=date.today()+timedelta(days=7))
    inventory_line_ids = fields.One2many('weekly.stockist.call.inventory.line', 'stockist_call_inv_id', "Inventory Product")
    order_line_ids = fields.One2many('weekly.stockist.call.order.line', 'stockist_call_ord_id', "Order Product")
    chemistwise_product_line_ids = fields.One2many('weekly.stockist.chemistwise.product', 'stockist_call_chemistwise_id', "Chemistwise Movement")
    stockist_work_with_ids = fields.Many2many('hr.employee', 'weekly_stockist_work_with', 'weekly_stockist_work_id', 'employee_id', string='Work With Whom')
    remark = fields.Text("Remark")
    telephonic_flag = fields.Boolean("Telephonic Call")
    reasons = fields.Selection([('due to rain', 'Due To rain'),('personal reason', 'Personal Reason')], 'Select Reason')
    
    @api.cr_uid_ids_context
    def _employee_get(self, cr, uid, context=None):
        emp_id = context.get('default_employee_id', False)
        if emp_id:
            return emp_id
        ids = self.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)], context=context)
        if ids:
            return ids[0]
        return False
     
    _defaults = {
     'employee_id' : _employee_get,
     }
     
class weekly_stockist_call_inventory_line(models.Model):
    _name = 'weekly.stockist.call.inventory.line'
     
    stockist_call_inv_id = fields.Many2one('weekly.stockist.call')
    product_id = fields.Many2one('product.product', "Product")
    inv_prod_quantity = fields.Integer("Quantity", default=0)
    state = fields.Selection([('damaged','Damaged'),('expire','Expire'),('normal','Normal'),('return','Return')])
     
    _defaults = {
     'state' : 'normal'
     }
     
class weekly_stockist_call_order_line(models.Model):
    _name = 'weekly.stockist.call.order.line'
     
    stockist_call_ord_id = fields.Many2one('weekly.stockist.call')
    product_id = fields.Many2one('product.product', "Product")
    ord_prod_quantity = fields.Integer("Quantity", default=0)
    last_mnth_qty = fields.Integer("Last Month Quantity", default=0, readonly=True)
    till_date_quantity = fields.Integer("Till Date quantity", default=0, readonly=True)
    superstockist_qty = fields.Integer("Superstockist Quantity", default=0, readonly=True)
    scheme_product_id = fields.Many2one('scheme.product', "Scheme")
    
class weekly_stockist_chemistwise_product(models.Model):
    _name = 'weekly.stockist.chemistwise.product'
     
    stockist_call_chemistwise_id = fields.Many2one('weekly.stockist.call')
    chemist_partner_id = fields.Many2one('res.partner', "Chemist")
    product_id = fields.Many2one('product.product', "Product")
    quantity = fields.Integer("Quantity", default=0)
    
class incentive_type(models.Model):
    _name = 'incentive.type'
    
    name = fields.Char("Name")
    description = fields.Text("Description")
    
class incentive(models.Model):
    _name = 'incentive'
    _rec_name = 'incentive_date'
    
    incentive_type_id = fields.Many2one('incentive.type', "Incentive Type")
    incentive_date = fields.Date("Date")
    employee_id = fields.Many2one('hr.employee', "Employee")
    amount = fields.Float("Amount", digits_compute=dp.get_precision('Product Price'))
    remark = fields.Text("Remark")
    
    
class disbursement(models.Model):
    _name = 'disbursement'
    _rec_name = 'disbursement_date'
    
    disbursement_date = fields.Date("Date")
    employee_id = fields.Many2one('hr.employee', "Employee")
    amount = fields.Float("Amount", digits_compute=dp.get_precision('Product Price'))
    remark = fields.Text("Remark")
