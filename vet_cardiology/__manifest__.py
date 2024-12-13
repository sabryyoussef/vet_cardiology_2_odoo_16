# -*- coding: utf-8 -*-
{
    'name': "Veterinary Cardiology",

    'summary': """
        Veterinary cardiology diagnostic tools and algorithms for cats and dogs""",

    'description': """
<div class="section" style="max-width: 84%; margin: 0 8%;">
    <h2 class="oe_slogan" style="color:#875A7B; text-align: center; margin-bottom: 20px;">Complete Veterinary Cardiology Module</h2>
    <h3 class="oe_slogan" style="margin-bottom: 20px;">Comprehensive Cardiac Diagnostic Tools for Veterinary Practice</h3>
    
    <div class="oe_row">
        <div class="oe_span12">
            <div class="panel panel-primary" style="border: 1px solid #875A7B; border-radius: 8px; padding: 15px; margin-bottom: 20px;">
                <h3 class="panel-title" style="color:#875A7B;">Key Features</h3>
                <ul class="list-unstyled">
                    <li style="margin: 8px 0;"><i class="fa fa-check-circle" style="color: #875A7B;"></i> Heart murmur diagnosis for cats and dogs</li>
                    <li style="margin: 8px 0;"><i class="fa fa-check-circle" style="color: #875A7B;"></i> Brady/Tachycardia assessment</li>
                    <li style="margin: 8px 0;"><i class="fa fa-check-circle" style="color: #875A7B;"></i> Pulse evaluation tools</li>
                    <li style="margin: 8px 0;"><i class="fa fa-check-circle" style="color: #875A7B;"></i> Cardiac arrhythmia analysis</li>
                    <li style="margin: 8px 0;"><i class="fa fa-check-circle" style="color: #875A7B;"></i> Interactive diagnostic algorithms</li>
                </ul>
            </div>
        </div>
    </div>

    <div class="oe_row">
        <div class="oe_span12">
            <h3 class="oe_slogan" style="color:#875A7B;">Heart Murmur Diagnosis</h3>
            <div class="oe_demo oe_screenshot">
                <img class="img img-fluid" src="/vet_cardiology/static/description/screen1.png"/>
            </div>
        </div>
    </div>

    <div class="oe_row">
        <div class="oe_span12">
            <h3 class="oe_slogan" style="color:#875A7B;">Cardiac Assessment Tools</h3>
            <div class="oe_demo oe_screenshot">
                <img class="img img-fluid" src="/vet_cardiology/static/description/screen2.png"/>
            </div>
        </div>
    </div>

    <div class="oe_row">
        <div class="oe_span12">
            <h3 class="oe_slogan" style="color:#875A7B;">Interactive Diagnostic Interface</h3>
            <div class="oe_demo oe_screenshot">
                <img class="img img-fluid" src="/vet_cardiology/static/description/screen3.png"/>
            </div>
        </div>
    </div>

    <div class="oe_row">
        <div class="oe_span12">
            <div class="alert alert-info" style="border-radius: 8px; margin-top: 20px;">
                <h3 style="color:#875A7B;">Benefits</h3>
                <ul class="list-unstyled">
                    <li style="margin: 8px 0;"><i class="fa fa-star" style="color: #875A7B;"></i> Streamlined cardiac diagnosis process</li>
                    <li style="margin: 8px 0;"><i class="fa fa-star" style="color: #875A7B;"></i> Evidence-based diagnostic algorithms</li>
                    <li style="margin: 8px 0;"><i class="fa fa-star" style="color: #875A7B;"></i> User-friendly interface for quick assessment</li>
                    <li style="margin: 8px 0;"><i class="fa fa-star" style="color: #875A7B;"></i> Comprehensive reporting system</li>
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
