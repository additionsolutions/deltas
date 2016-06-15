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

class addsol_ppp(models.Model):
    _name = 'addsol.ppp'
    _rec_name = 'ppp_date'
    
    ppp_date = fields.Date("Date", default=date.today())
    mode = fields.Selection([('After', 'After'),('Before', 'Before')], 'Mode')
    asm_id = fields.Many2one('hr.employee', "ASM")
    mr_id = fields.Many2one('hr.employee', "MR")
    region_id = fields.Many2one('addsol.region.state', "HQ")
    partner_id = fields.Many2one('res.partner', "Customer")
    nature = fields.Selection([('campaign', 'Campaign'),('industry promotion', 'Industry Promotion'),('roadshow', 'Roadshow'),('counter promotion', 'Counter Promotion')], 'Nature')
    total_expected_amount = fields.Float("Expected Amount", defualt=0.0)
    period = fields.Char("Period")
    period_comment = fields.Char("Comment")
    promotional_allowance = fields.Float("Promotional Expenses")
    allowance_percentage = fields.Float("Allowance Percenatge")
    allowance_nature = fields.Selection([('cash', 'Cash'),('gift', 'Gift'),('other', 'Other')], 'Allowance Nature')
    comment_nature = fields.Char("Other Comment")
    status = fields.Selection([('Submitted', 'Submitted'),('Approved', 'Approved'),('Pending', 'Pending'),('Rejected', 'Rejected')])
    remark = fields.Text("Remark")
    payment_date = fields.Date("Payment Date")
    payment_amount = fields.Float("Payment Amount")
    addsol_ppp_line_ids = fields.One2many('addsol.ppp.line', 'addsol_ppp_id', "PPP Line")
    addsol_ppp_record_line_ids = fields.One2many('addsol.ppp.record.line', 'addsol_ppp_id', "PPP Record Line")
    
class addsol_ppp_line(models.Model):
    _name = 'addsol.ppp.line'
       
    addsol_ppp_id = fields.Many2one('addsol.ppp')
    product_id = fields.Many2one('product.product', "Product")
    expected_quantity = fields.Integer("Quantity", default=0)
    expected_amount = fields.Float("Expected Amount", default=0.0)


class addsol_ppp_record_line(models.Model):
	_name = 'addsol.ppp.record.line'
	
	addsol_ppp_id = fields.Many2one('addsol.ppp')
	record_amount = fields.Float("Expected Amount", default=0.0)
	attach_file = fields.Binary("Attachment File")
	
# class addsol_ppp_records(models.Model):
    # _name = 'addsol.ppp.records'
    # _rec_name = 'record_date'
    
    
    # #@api.model
    # #def _get_default_image(self, is_company, colorize=False):
    # #    if getattr(threading.currentThread(), 'testing', False) or self.env.context.get('install_mode'):
    # #        return False

    # #    img_path = openerp.modules.get_module_resource('base', 'static/src/img', 'company_image.png' if is_company else 'avatar.png')
    # #    with open(img_path, 'rb') as f:
    # #        image = f.read()

        # # colorize user avatars
    # #    if not is_company and colorize:
    # #        image = tools.image_colorize(image)

    # #    return tools.image_resize_image_big(image.encode('base64'))
		
	# #@api.depends('image')
	# #def _compute_images(self):
	# #	for rec in self:
	# #		rec.image_medium = tools.image_resize_image_medium(rec.image)
	# #		rec.image_small = tools.image_resize_image_small(rec.image)
			
	# #def _inverse_image_medium(self):
	# #	for rec in self:
	# #		rec.image = tools.image_resize_image_big(rec.image_medium)

	# #def _inverse_image_small(self):
	# #	for rec in self:
	# #		rec.image = tools.image_resize_image_big(rec.image_small)
			
    
    # record_date = fields.Date("Date", default=date.today())
    # asm_id = fields.Many2one('hr.employee', "ASM")
    # mr_id = fields.Many2one('hr.employee', "MR")
    # partner_id = fields.Many2one('res.partner', "Customer")
    # # image: all image fields are base64 encoded and PIL-supported
    # #image = fields.Binary("Image", attachment=True, help="This field holds the image used as avatar for this contact, limited to 1024x1024px", default=lambda self: self._get_default_image(False, True))
    # amount = fields.Float("Amount", default=0.0)
    # attach_file = fields.Binary("Attachment File")
    # #image_medium = fields.Binary("Medium-sized image",compute='_compute_images', inverse='_inverse_image_medium', store=True, attachment=True,
    # #    help="Medium-sized image of this contact. It is automatically "\
    # #         "resized as a 128x128px image, with aspect ratio preserved. "\
    # #         "Use this field in form views or some kanban views.")
    # #image_small = openerp.fields.Binary("Small-sized image",
        # #compute='_compute_images', inverse='_inverse_image_small', store=True, attachment=True,
        # #help="Small-sized image of this contact. It is automatically "\
             # #"resized as a 64x64px image, with aspect ratio preserved. "\
             # #"Use this field anywhere a small image is required.")
			 
    # #_defaults = {
    # #    'image': True,
    # #}
