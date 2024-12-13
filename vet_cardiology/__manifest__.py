# -*- coding: utf-8 -*-
{
    'name': "Veterinary Cardiology",

    'summary': """
        Veterinary cardiology diagnostic tools and algorithms for cats and dogs""",

    'description': """
<div class="row">
    <div class="col-md-12">
        <div class="mt16 mb16">
            <h2 class="text-center" style="color: #875A7B;">Complete Veterinary Cardiology Module</h2>
        </div>
        <div class="oe_demo oe_screenshot">
            <img class="img img-fluid" src="/vet_cardiology/static/description/banner.png"/>
        </div>
        <div class="mt32">
            <h3 class="text-center" style="color: #875A7B;">Key Features</h3>
            <div class="mt16">
                <ul class="list-unstyled">
                    <li class="mb8">
                        <i class="fa fa-check-circle" style="color: #875A7B;"></i>
                        Heart murmur diagnosis for cats and dogs
                    </li>
                    <li class="mb8">
                        <i class="fa fa-check-circle" style="color: #875A7B;"></i>
                        Brady/Tachycardia assessment
                    </li>
                    <li class="mb8">
                        <i class="fa fa-check-circle" style="color: #875A7B;"></i>
                        Pulse evaluation tools
                    </li>
                    <li class="mb8">
                        <i class="fa fa-check-circle" style="color: #875A7B;"></i>
                        Cardiac arrhythmia analysis
                    </li>
                    <li class="mb8">
                        <i class="fa fa-check-circle" style="color: #875A7B;"></i>
                        Interactive diagnostic algorithms
                    </li>
                </ul>
            </div>
        </div>
    </div>
</div>
    """,

    'author': "Vet Sabry Youssef_01000059085",
    'website': "https://www.vetbrains.com",

    'category': 'Healthcare/Veterinary',
    'version': '1.0.0',

    'images': [
        'static/description/banner.png',
        'static/description/screenshot1.png',
        'static/description/screenshot2.png',
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
