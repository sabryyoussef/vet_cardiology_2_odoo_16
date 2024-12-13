# -*- coding: utf-8 -*-
{
    'name': "Veterinary Cardiology",

    'summary': """
        Veterinary cardiology diagnostic tools and algorithms for cats and dogs""",

    'description': """
        <div class="container">
            <h2 class="oe_slogan">Complete Veterinary Cardiology Module</h2>
            <div class="oe_span12">
                <div class="oe_demo oe_picture oe_screenshot">
                    <p>Comprehensive suite of cardiology tools featuring:</p>
                    <ul>
                        <li>Heart murmur diagnosis for cats and dogs</li>
                        <li>Brady/Tachycardia assessment</li>
                        <li>Pulse evaluation tools</li>
                        <li>Cardiac arrhythmia analysis</li>
                        <li>Interactive diagnostic algorithms</li>
                    </ul>
                </div>
            </div>
        </div>
    """,

<<<<<<< HEAD
    'author': "Vet Sabry Youssef_01000059085",
=======
    'author': "Vet Sabry Youssef _01000059085",
>>>>>>> 1c2514af4673cb52305e10ec316abf5f8b26a48b
    'website': "https://www.vetbrains.com",

    'category': 'Healthcare/Veterinary',
    'version': '1.0.0',
    
    # Icon and images
    'icon': '/vet_cardiology/static/discription/assets/icons/icon.png',
    'images': ['/vet_cardiology/static/discription/assets/icons/cover.png'],
    
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
    
    'icon': '/vet_cardiology/static/img/sabry_cardiology_module.png',  # Add this line for the image
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
