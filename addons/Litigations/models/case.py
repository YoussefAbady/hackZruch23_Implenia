from odoo import models,fields,api
from datetime import date
import logging


_logger = logging.getLogger(__name__)



class case(models.Model):
    _name = "case"
    _description = "Litigation Case"


    #Project Info
    division_id = fields.Many2one(comodel_name='division', string='Division')
    country_id = fields.Many2one(comodel_name='country', string='Country')
    investment_center_id = fields.Many2one(comodel_name='investment.center', string='Investment Center')
    PSP = fields.Char(string='PSP') #??
    description = fields.Text(string='Description')
    is_RDA = fields.Boolean(string='RDA') #??

    #Case Details
    number = fields.Char(string='Number') # to be unique
    name = fields.Char(string='Name')
    case_type = fields.Selection(string='Case Type', selection=[('EXP', 'Expected'), ('ACT', 'Actual')])
    case_ownership = fields.Selection(string='Case Ownership', selection=[('AGN', 'Against Company'), ('BY', 'By Company')])
    subject_matter = fields.Char(string='Subject matter')
    currency_id = fields.Many2one(comodel_name='currency', string='Currency')
    currency_code = fields.Char(related='currency_id.code')
    

    # Handlers
    bus_res_id = fields.Many2one(comodel_name='res.users', string='Business Responsible')
    fin_res_id = fields.Many2one(comodel_name='res.users', string='Legal Responsible')
    leg_res_id = fields.Many2one(comodel_name='res.users', string='Finance Responsible')

    claimant = fields.Char(string='Claimant')
    claim_respondent  = fields.Char(string='Claim Respondent')
    counter_party_relation = fields.Selection(string='Relation of Counter Party', selection=[('CLI', 'Client'), ('SUB', 'Sub-Contractor'),('AUTH', 'Authorities ')])


    # Legal Assessment
    expected_enforceable_amount = fields.Integer(string='Expected Enforceable Amount',dafualt='0')
    accounting_considered_amount = fields.Integer(string='Accounting Considered amount')
    case_situation = fields.Selection(string='Case Situation', selection=[('OPP', 'Opportunity'), ('RSK', 'Risk')])

    # Costs
    expected_legal_cost = fields.Integer(string='Expected Legal Cost')
    actual_legal_cost = fields.Integer(string='Actual Legal Cost')
    expected_court_cost = fields.Integer(string='Expected Court Cost')
    actual_court_cost = fields.Integer(string='Actual Court Cost')

    #Dates
    proceeding_start = fields.Date(string='Proceeding Start')
    proceeding_end = fields.Date(string='Proceeding End')

    #Intersets
    interest_active_date = fields.Date(string='Interest Active Date')
    interest_rate = fields.Float(string='Interest Rate (%)',default='0')
    interest_days = fields.Integer(compute='_compute_interest_days')
    
    interests_amount = fields.Float(string='Interests Amount',compute="_compute_interests_amount",default=0)
    total_growth = fields.Float(string='Total Amount',compute="_compute_total_growth",default=0)
    total_net = fields.Float(string='Total Net',compute="_compute_total_net",default=0)


    # Case Status

    proceeding_instance = fields.Integer(string='Proceeding Instance')
    proceeding_status = fields.Selection(string='Proceeding Status', selection=[('BRF', 'Exchange of briefs'),
                                                                                ("RED","Judgement rendered "),
                                                                                 ('EVD', 'Evidence preservation'),
                                                                                 ('SET', 'Settlement discussions')])
    
    proceeding_note = fields.Text(string='Proceeding Notes')

    dispute_value = fields.Integer(string='Value in dispute (k)')
    dispute_value_share = fields.Float(string='Dispute Value Share (%)')
    actual_dispute_value = fields.Float(string='Actual Dispute Value',compute="_compute_actual_dispute_value",default=0)

    status = fields.Selection(string='Case Status', selection=[('ACT', 'Active'), ('CLS', 'Closed'),('PEN', 'Pending')])


    # Followup
    comments = fields.Text(string='Comments')
    next_milesstone = fields.Char(string='Next Milestone')
    next_milestone_duedate = fields.Date(string='Next Milestone Due Date')

    


    @api.depends("dispute_value","dispute_value_share")
    def _compute_actual_dispute_value(self):
        for record in self:
            record.actual_dispute_value = record.dispute_value * record.dispute_value_share/100

    @api.depends("interest_active_date","proceeding_end",)
    def _compute_interest_days(self):
        for record in self:
            record.interest_days = 0

        if(record.interest_active_date == False):
            return

        if(record.proceeding_end == False):
            return
        
        record.interest_days = (record.proceeding_end - record.interest_active_date).days

    @api.depends("interest_active_date","interest_rate","expected_enforceable_amount","proceeding_end")
    def _compute_interests_amount(self):
        for record in self:
            record.interests_amount = 0

        if(record.interest_active_date == False):
            return

        if(record.proceeding_end == False):
            return
        
        inters_days = (record.proceeding_end - record.interest_active_date).days
        record.interests_amount = (record.interest_rate/(100*365)) * inters_days * record.expected_enforceable_amount

      
    
    @api.depends("interests_amount","expected_enforceable_amount")
    def _compute_total_growth(self):
        for record in self:
            record.total_growth = 0
            record.total_growth = record.interests_amount + record.expected_enforceable_amount

        
    @api.depends("total_growth","expected_legal_cost","expected_court_cost")
    def _compute_total_net(self):
        for record in self:
            record.total_net = 0
            record.total_net = record.total_growth - ( record.expected_legal_cost + record.expected_court_cost)
      
    
    

    

    
    
    

    

    
    

