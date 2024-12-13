from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TachyarrhythmiaAlgorithm(models.Model):
    _name = 'veterinary.tachyarrhythmia'
    _description = 'Tachyarrhythmia Diagnostic Algorithm'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Determine the display order"
    )

    name = fields.Char(
        string='Name',
        required=True,
        help='Name or identifier for the tachyarrhythmia record'
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
    species = fields.Selection([
        ('dog', 'Dog'),
        ('cat', 'Cat')
    ], string='Species', required=True, tracking=True)
    heart_rate = fields.Integer(string='Heart Rate (bpm)', required=True, tracking=True)
    rhythm_regular = fields.Boolean(string='Regular Rhythm', tracking=True)
    
    # ECG Parameters
    complex_type = fields.Selection([
        ('supraventricular', 'Supraventricular'),
        ('ventricular', 'Ventricular')
    ], string='Complex Type')
    p_wave_visible = fields.Boolean(string='P Waves Visible')
    
    # Results
    diagnosis = fields.Text(string='Diagnosis', readonly=True)
    treatment = fields.Text(string='Treatment Plan', readonly=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('diagnosed', 'Diagnosed')
    ], default='draft', string='Status', tracking=True)

    @api.constrains('heart_rate')
    def _check_heart_rate(self):
        for record in self:
            if record.heart_rate <= 0:
                raise ValidationError("Heart rate must be greater than 0")

    def assess_heart_rate(self):
        self.ensure_one()
        if self.species == "dog" and self.heart_rate > 160:
            return True
        elif self.species == "cat" and self.heart_rate > 220:
            return True
        return False

    def diagnose(self):
        self.ensure_one()
        treatment_list = []
        
        if not self.rhythm_regular:
            self.diagnosis = "Atrial fibrillation"
            treatment_list = [
                "Decrease heart rate with agents (e.g., digoxin, calcium-channel blockers, β-blockers)",
                "Consider rhythm control via transthoracic electric cardioversion"
            ]
        else:
            if self.complex_type == "ventricular":
                self.diagnosis = "Ventricular tachycardia"
                treatment_list = [
                    "Immediate therapy if VT is rapid, multiform, and produces clinical signs—IV lidocaine or procainamide",
                    "Identify and treat underlying heart disease",
                    "Treat underlying systemic diseases",
                    "Withdraw possible offending drugs (e.g., digoxin)",
                    "Correct electrolyte imbalances",
                    "Sotalol, mexiletine, or amiodarone for long-term maintenance therapy",
                    "24-hour Holter monitoring to determine therapeutic efficacy"
                ]
            elif self.complex_type == "supraventricular":
                if self.p_wave_visible:
                    self.diagnosis = "Sinus tachycardia"
                    treatment_list = ["Treat underlying causes"]
                else:
                    self.diagnosis = "Sustained or Paroxysmal SVT"
                    treatment_list = [
                        "Vagal maneuvers (e.g., carotid sinus massage, ocular pressure, precordial thump)",
                        "IV boluses of procainamide, diltiazem, esmolol",
                        "Transthoracic electrical cardioversion"
                    ]
        
        self.treatment = "\n".join(f"- {item}" for item in treatment_list)
        return True

    def action_diagnose(self):
        self.ensure_one()
        if self.assess_heart_rate():
            self.diagnose()
            self.state = 'diagnosed'
        else:
            self.diagnosis = "Heart rate does not indicate tachyarrhythmia."
            self.treatment = "No treatment required for tachyarrhythmia."
            self.state = 'diagnosed'
        return True

    def action_reset(self):
        self.ensure_one()
        self.write({
            'diagnosis': False,
            'treatment': False,
            'complex_type': False,
            'p_wave_visible': False,
            'state': 'draft'
        })
        return True