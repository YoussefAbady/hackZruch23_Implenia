from odoo import models,fields,api

class investmentCenter(models.Model):
    _name = "investment.center"
    _description = "Investment Center"

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')
    
    
    

