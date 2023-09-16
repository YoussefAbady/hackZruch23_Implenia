from odoo import models,fields,api

class division(models.Model):
    _name = "division"
    _description = "Division"

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')
    
    
    

