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

    'author': "Your Company Name",
    'website': "https://www.yourcompany.com",

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
        # 'views/tachyarrhythmia_wizard_views.xml',
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

    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
