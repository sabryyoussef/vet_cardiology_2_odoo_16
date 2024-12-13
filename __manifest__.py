# -*- coding: utf-8 -*-
{
    'name': "Veterinary Cardiology",

    'summary': """
        Veterinary cardiology diagnostic tools and algorithms for cats and dogs""",

    'description': """
        Complete veterinary cardiology module featuring:
        * Heart murmur diagnosis for cats and dogs
        * Brady/Tachycardia assessment
        * Pulse evaluation tools
        * Cardiac arrhythmia analysis
        * Interactive diagnostic algorithms
    """,

    'author': "vet.sabry youssef_01000059085",
    'website': "https://www.vetbrains.com",

    'category': 'Healthcare/Veterinary',
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'mail',
        'web',
        'calendar',
    ],

    # always loaded
    'data': [
        # Security
        'security/security.xml',
        'security/ir.model.access.csv',
# -*- coding: utf-8 -*-
{
    'name': "Veterinary Cardiology",
    'summary': """
        Professional veterinary cardiology diagnostic tools and algorithms for cats and dogs
    """,

    'description': """
        Complete veterinary cardiology module featuring:
        * Heart murmur diagnosis for cats and dogs
        * Brady/Tachycardia assessment
        * Pulse evaluation tools
        * Cardiac arrhythmia analysis
        * Interactive diagnostic algorithms
        * Comprehensive cardiology reports
        * Patient history tracking
        * Treatment recommendations
    """,

    'author': "vet sabry youssef 01000059085",
    'website': "https://www.vetbrains.com",
    'support': "sabryyoussef11@gmail.com",

    'category': 'Healthcare/Veterinary',
    'version': '16.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'mail',
        'web',
        'calendar',
        'report_xlsx',
    ],

    # always loaded
    'data': [
        # Security
        'security/security.xml',
        'security/ir.model.access.csv',
        
        # Data
        'data/sequence/sequence.xml',
        
        # Views
        'views/animal_algorithm.xml',
        'views/cardiology_brady_tachy_cardia.xml',
        'views/cardiology_heart_murmur_cats.xml',
        'views/cardiology_heart_murmur_dogs_2.xml',
        'views/cardiology_pulse_ultration_2.xml',
        'views/cardiology_tachy_arythmia_2.xml',
        'views/image_popup_view.xml',
        'views/views.xml',
        'views/templates.xml',
    ],

    'demo': [
        'demo/demo.xml',
        'demo/cardiology_brady_tachy_cardia_demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cardiology_sc/static/src/js/**/*',
            'cardiology_sc/static/src/xml/**/*',
            'cardiology_sc/static/src/scss/**/*',
        ],
    },

    'images': ['static/description/banner.png'],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    
    'price': 0.0,
    'currency': 'EUR',
    
    # Odoo version indication
    'odoo_version': '16.0',
}
        # Data
        'data/sequence/sequence.xml',

        # Views
        'views/animal_algorithm.xml',
        'views/cardiology_brady_tachy_cardia.xml',
        'views/cardiology_heart_murmur_cats.xml',
        'views/cardiology_heart_murmur_dogs_2.xml',
        'views/cardiology_pulse_ultration_2.xml',
        'views/cardiology_tachy_arythmia_2.xml',
        'views/image_popup_view.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/vetcalc_view.xml',

        #wizard
        'wizard/tachyarrhythmia_wizard_views.xml',
        'views/dashboard_view.xml',
    ],

    'demo': [
        'demo/demo.xml',
        'demo/cardiology_brady_tachy_cardia_demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'cardiology_sc/static/src/js/**/*',
            'cardiology_sc/static/src/xml/**/*',
            'cardiology_sc/static/src/scss/**/*',
            '/cardiology_sc/static/src/css/style.css',
            # 'cardiology_sc/static/src/css/style.css',
            '/cardiology_sc/static/src/css/dashboard.css',
        ],
    },

    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
