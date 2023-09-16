from odoo import models,fields,api

class country(models.Model):
    _name = "country"
    _description = "Country"

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')

    
    

