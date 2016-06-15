# -*- coding: utf-8 -*-
from openerp import http

# class AddsolProduct(http.Controller):
#     @http.route('/addsol_product/addsol_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/addsol_product/addsol_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('addsol_product.listing', {
#             'root': '/addsol_product/addsol_product',
#             'objects': http.request.env['addsol_product.addsol_product'].search([]),
#         })

#     @http.route('/addsol_product/addsol_product/objects/<model("addsol_product.addsol_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('addsol_product.object', {
#             'object': obj
#         })