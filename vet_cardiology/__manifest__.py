# -*- coding: utf-8 -*-
{
    'name': "Veterinary Cardiology",

    'summary': """
        Veterinary cardiology diagnostic tools and algorithms for cats and dogs""",

    'description': """
Veterinary Cardiology Module
===========================

A comprehensive suite of diagnostic tools for veterinary cardiology, including:

* Heart murmur diagnosis for cats and dogs
* Brady/Tachycardia assessment
* Pulse evaluation tools
* Cardiac arrhythmia analysis
* Interactive diagnostic algorithms

For detailed information and screenshots, please visit the module's page.
    """,

    'author': "Vet Sabry Youssef_01000059085",
    'website': "https://www.vetbrains.com",

    'category': 'Healthcare/Veterinary',
    'version': '1.0.0',

    'images': [
        'static/description/banner.png',
        'static/description/screen1.png',
        'static/description/screen2.png',
        'static/description/screen3.png',
    ],

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
        'views/assets.xml',
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
            # JavaScript
            'vet_cardiology/static/src/js/cardiology_dashboard.js',
            
            # SCSS Styles
            'vet_cardiology/static/src/scss/dashboard.scss',
            'vet_cardiology/static/src/scss/style.scss',
        ],
    },
    
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
