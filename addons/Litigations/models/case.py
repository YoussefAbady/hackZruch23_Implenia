from odoo import models,fields,api
from datetime import date
import logging


_logger = logging.getLogger(__name__)



class case(models.Model):
    _name = "case"
    _description = "Litigation Case"
    _inherit = ['mail.thread', 'mail.activity.mixin']




    #Project Info
    division_id = fields.Many2one(comodel_name='division', string='Division',tracking=True)
    country_id = fields.Many2one(comodel_name='country', string='Country',tracking=True)
    investment_center_id = fields.Many2one(comodel_name='investment.center', string='Investment Center',tracking=True)
    PSP = fields.Char(string='PSP',tracking=True) #??
    is_RDA = fields.Boolean(string='RDA',tracking=True) #??

    #Case Details
    description = fields.Text(string='Description',tracking=True)
    number = fields.Char(string='Number',tracking=True) # to be unique
    name = fields.Char(string='Name',tracking=True)
    case_type = fields.Selection(string='Case Type', selection=[('EXP', 'Expected'), ('ACT', 'Actual')],tracking=True)
    case_ownership = fields.Selection(string='Case Ownership', selection=[('AGN', 'Against Company'), ('BY', 'By Company')],tracking=True)
    subject_matter = fields.Char(string='Subject matter',tracking=True)
    currency_id = fields.Many2one(comodel_name='currency', string='Currency',tracking=True)
    currency_code = fields.Char(related='currency_id.code',tracking=True)
    

    # Handlers
    bus_res_id = fields.Many2one(comodel_name='res.users', string='Business Responsible',tracking=True)
    fin_res_id = fields.Many2one(comodel_name='res.users', string='Legal Responsible',tracking=True)
    leg_res_id = fields.Many2one(comodel_name='res.users', string='Finance Responsible',tracking=True)

    claimant = fields.Char(string='Claimant',tracking=True)
    claim_respondent  = fields.Char(string='Claim Respondent',tracking=True)
    counter_party_relation = fields.Selection(string='Relation of Counter Party', selection=[('CLI', 'Client'), ('SUB', 'Sub-Contractor'),('AUTH', 'Authorities ')],tracking=True)


    # Legal Assessment
    expected_enforceable_amount = fields.Integer(string='Expected Enforceable Amount',dafualt='0',tracking=True)
    accounting_considered_amount = fields.Integer(string='Accounting Considered amount',tracking=True)
    case_situation = fields.Selection(string='Case Situation', selection=[('OPP', 'Opportunity'), ('RSK', 'Risk')],tracking=True)

    # Costs
    expected_legal_cost = fields.Integer(string='Expected Legal Cost',tracking=True)
    actual_legal_cost = fields.Integer(string='Actual Legal Cost',tracking=True)
    expected_court_cost = fields.Integer(string='Expected Court Cost',tracking=True)
    actual_court_cost = fields.Integer(string='Actual Court Cost',tracking=True)

    #Dates
    proceeding_start = fields.Date(string='Proceeding Start',tracking=True)
    proceeding_end = fields.Date(string='Proceeding End',tracking=True)

    #Intersets
    interest_active_date = fields.Date(string='Interest Active Date',tracking=True)
    interest_rate = fields.Float(string='Interest Rate (%)',default='0',tracking=True)
    interest_days = fields.Integer(compute='_compute_interest_days',tracking=True)
    
    interests_amount = fields.Float(string='Interests Amount',compute="_compute_interests_amount",default=0)
    total_growth = fields.Float(string='Total Amount',compute="_compute_total_growth",default=0)
    total_net = fields.Float(string='Total Net',compute="_compute_total_net",default=0)


    # Case Status

    proceeding_instance = fields.Integer(string='Proceeding Degree',tracking=True)
    proceeding_status = fields.Selection(string='Proceeding Status', selection=[('BRF', 'Exchange of briefs'),
                                                                                ("RED","Judgement rendered "),
                                                                                 ('EVD', 'Evidence preservation'),
                                                                                 ('SET', 'Settlement discussions')],tracking=True)
    
    proceeding_note = fields.Text(string='Proceeding Notes',tracking=True)

    dispute_value = fields.Integer(string='Value in dispute (k)',tracking=True)
    dispute_value_share = fields.Float(string='Dispute Value Share (%)',tracking=True)
    actual_dispute_value = fields.Float(string='Actual Dispute Value',compute="_compute_actual_dispute_value",default=0,tracking=True)

    status = fields.Selection(string='Case Status', selection=[('ACT', 'Active'), ('CLS', 'Closed'),('PEN', 'Pending')],tracking=True)


    # Followup
    comments = fields.Text(string='Comments',tracking=True)
    next_milesstone = fields.Char(string='Next Milestone',tracking=True)
    next_milestone_duedate = fields.Date(string='Next Milestone Due Date',tracking=True)

    


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
      
    
    

    

    
    
    

    

    
    

