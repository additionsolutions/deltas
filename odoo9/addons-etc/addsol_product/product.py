# -*- coding: utf-8 -*-

from openerp import fields, models

class Product(models.Model):
	
	_inherit = "product.template"
	
	name1 = fields.Char("Name 1", help="Enter Synonym 1")
	name2 = fields.Char("Name 2", help="Enter Synonym 2")
	name3 = fields.Char("Name 3", help="Enter Synonym 3")
	cas = fields.Char("CAS #", help="Enter CAS #")
	qa_required = fields.Boolean("QA required", help="Requires mandatory Quality Check after taking delivery from supplier")
	
	
class addsol_product_product(models.Model):
    _inherit = 'product.product'
    
    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        #name search method to search the product by using synonyms
        args.append(('|'))
        args.append(('|'))
        args.append(('|'))
        args.append(('|'))
        args.append(('name','ilike',name))
        args.append(('name1','ilike',name))
        args.append(('name2','ilike',name))
        args.append(('name3','ilike',name))
        args.append(('cas','ilike',name))
        return super(addsol_product_product,self).name_search(cr, user, '', args=args,operator='ilike', context=context, limit=limit)