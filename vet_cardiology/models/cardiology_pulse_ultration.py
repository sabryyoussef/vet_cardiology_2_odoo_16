from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PulseAlterationDiagnosis(models.Model):
    _name = 'veterinary.pulse.alteration'
    _description = 'Pulse Alteration Diagnosis'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Determine the display order"
    )

    animal_algorithm_id = fields.Many2one(
        'animal.algorithm',
        string='Base Algorithm Reference',
        required=True,
        ondelete='cascade',
        tracking=True
    )
        # Add related field for animal type
    animal_type = fields.Selection(
        related='animal_algorithm_id.animal_type',
        string='Animal Type',
        store=True
    )


    # Basic Parameters
    name = fields.Char(string='Reference', readonly=True, copy=False, default='New')
    palpable_pulse = fields.Boolean(string='Palpable Pulse', tracking=True)
    heart_status = fields.Selection([
        ('normal', 'Normal'),
        ('bradycardia', 'Bradycardia'),
        ('tachycardia', 'Tachycardia'),
        ('dysrhythmia', 'Dysrhythmia')
    ], string='Heart Status', required=True, tracking=True)
    
    # ECG Parameters
    qrs_amplitude = fields.Selection([
        ('normal', 'Normal'),
        ('small', 'Small'),
        ('large', 'Large')
    ], string='QRS Amplitude')
    
    # Diagnostic Results
    diagnosis = fields.Text(string='Diagnosis', readonly=True)
    differentials = fields.Text(string='Differential Diagnoses', readonly=True)
    recommendations = fields.Text(string='Recommendations', readonly=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('diagnosed', 'Diagnosed'),
        ('emergency', 'Emergency/CPR')
    ], default='draft', string='Status', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('veterinary.pulse.alteration') or 'New'
        return super(PulseAlterationDiagnosis, self).create(vals)

    def _get_dysrhythmia_differentials(self):
        return """
- Hypovolemia
- Hypothermia
- Hypothyroidism
- Depressed myocardial contractility
        """

    def _get_bradycardia_differentials(self):
        return """
- Sinus bradycardia
- Atrioventricular block
- Hypothyroidism
- Hypothermia
- Idioatrial/idioventricular rhythm
        """

    def _get_tachycardia_differentials(self):
        return """
- Sinus tachycardia
- Ventricular tachycardia
- Supraventricular tachycardia
- Atrial fibrillation
        """

    def action_diagnose(self):
        self.ensure_one()
        
        # Reset previous results
        self.write({
            'diagnosis': False,
            'differentials': False,
            'recommendations': False
        })
        
        # Check for emergency conditions first
        if not self.palpable_pulse:
            self.write({
                'diagnosis': 'No palpable pulse detected - Emergency situation',
                'recommendations': 'Initiate CPR immediately',
                'state': 'emergency'
            })
            return True

        # Process based on heart status
        if self.heart_status == 'dysrhythmia':
            self.write({
                'diagnosis': 'Dysrhythmia detected',
                'differentials': self._get_dysrhythmia_differentials(),
                'recommendations': 'Further cardiac evaluation recommended'
            })
        
        elif self.qrs_amplitude == 'small':
            self.write({
                'diagnosis': 'Small QRS amplitude detected',
                'recommendations': 'Perform pericardiocentesis if pericardial effusion is confirmed'
            })
        
        elif self.heart_status == 'normal':
            self.write({
                'diagnosis': 'Normal cardiac evaluation',
                'recommendations': 'No specific cardiac intervention required'
            })
        
        elif self.heart_status == 'bradycardia':
            self.write({
                'diagnosis': 'Bradycardia detected',
                'differentials': self._get_bradycardia_differentials(),
                'recommendations': 'Monitor cardiac status and investigate underlying causes'
            })
        
        elif self.heart_status == 'tachycardia':
            self.write({
                'diagnosis': 'Tachycardia detected',
                'differentials': self._get_tachycardia_differentials(),
                'recommendations': 'Evaluate for underlying cardiac conditions'
            })
        
        self.state = 'diagnosed'
        return True

    def action_reset(self):
        self.ensure_one()
        self.write({
            'diagnosis': False,
            'differentials': False,
            'recommendations': False,
            'state': 'draft'
        })
        return True