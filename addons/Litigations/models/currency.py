from odoo import models,fields,api

class currency(models.Model):
    _name = "currency"
    _description = "Currencies"

    code = fields.Char(string='Code')
    name = fields.Char(string='Name')

    
    

