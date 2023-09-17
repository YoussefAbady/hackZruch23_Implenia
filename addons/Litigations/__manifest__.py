{
    'name': 'Litigations',
    'version':'0.1',
    'category':'Legal',
    'description':'Implena Legal System',
    'author': "One of HackZurich Teams ( NOT FOR COMMERCIAL USE )",
    'depends' : ['mail','board'],
     'data': [
        'security/ir.model.access.csv',
        'data/country.csv',
        'data/investment.center.csv',
        'data/division.csv',
        'data/currency.csv',
        'views/litigations_country.xml',
        'views/litigations_division.xml',
        'views/litigations_currency.xml',
        'views/litigations_investment_center.xml',
        'views/litigations_case.xml',
        'views/litigations_menue.xml'
    ]
}