from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DogHeartMurmurDiagnosis(models.Model):
    _name = 'veterinary.dog.heart.murmur'
    _description = 'Dog Heart Murmur Diagnosis'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'display_name'

    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Determine the display order"
    )

    murmur_grade = fields.Selection([
        ('1', 'Grade I'),
        ('2', 'Grade II'),
        ('3', 'Grade III'),
        ('4', 'Grade IV'),
        ('5', 'Grade V'),
        ('6', 'Grade VI')
    ], string='Murmur Grade',
        required=True,
        tracking=True,
        help="Grade of the heart murmur from I to VI")

    # Basic Information
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

    display_name = fields.Char(compute='_compute_display_name', store=True)

    
    # Murmur Parameters
    location = fields.Selection([
        ('left_base', 'Left Base'),
        ('left_apex', 'Left Apex'),
        ('right_base', 'Right Base'),
        ('right_apex', 'Right Apex')
    ], string='Murmur Location', required=True, tracking=True)
    
    intensity = fields.Selection([
        ('1', 'Grade I'),
        ('2', 'Grade II'),
        ('3', 'Grade III'),
        ('4', 'Grade IV'),
        ('5', 'Grade V'),
        ('6', 'Grade VI')
    ], string='Murmur Intensity', required=True, tracking=True)
    
    murmur_type = fields.Selection([
        ('systolic', 'Systolic'),
        ('diastolic', 'Diastolic'),
        ('continuous', 'Continuous')
    ], string='Murmur Type', required=True, tracking=True)
    
    # Patient Information
    dog_weight = fields.Float(string='Dog Weight (kg)', required=True)
    age_group = fields.Selection([
        ('young', 'Young'),
        ('middle', 'Middle-aged'),
        ('older', 'Older')
    ], string='Age Group', required=True)
    
    clinical_signs = fields.Selection([
        ('none', 'None'),
        ('fever', 'Fever'),
        ('lameness', 'Lameness'),
        ('new_murmur', 'New Murmur')
    ], string='Clinical Signs', required=True)

    # Diagnostic Results
    diagnosis = fields.Text(string='Diagnosis', readonly=True)
    recommendation = fields.Text(string='Recommendation', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('diagnosed', 'Diagnosed')
    ], default='draft', string='Status', tracking=True)

    @api.depends('location', 'intensity', 'create_date')
    def _compute_display_name(self):
        for record in self:
            if record.create_date:
                record.display_name = f"Murmur Grade {record.intensity} - {record.location} ({record.create_date.strftime('%Y-%m-%d')})"
            else:
                record.display_name = f"New Murmur Diagnosis"

    def evaluate_murmur(self):
        self.ensure_one()
        diagnosis_text = []
        recommendation_text = []

        # Convert intensity to integer for comparison
        intensity = int(self.intensity)

        # Step 1: Initial check for murmur intensity
        if intensity >= 3:
            diagnosis_text.append("Murmur is grade III/VI or higher.")
            result = self._check_high_intensity_murmur()
        else:
            diagnosis_text.append("Murmur is grade II/VI or less.")
            result = self._check_low_intensity_murmur()
        
        diagnosis_text.extend(result.get('diagnosis', []))
        recommendation_text.extend(result.get('recommendation', []))

        self.diagnosis = "\n".join(diagnosis_text)
        self.recommendation = "\n".join(recommendation_text)
        self.state = 'diagnosed'
        
        return True

    def _check_high_intensity_murmur(self):
        diagnosis = []
        recommendation = []

        if self.location == 'left_base' and self.murmur_type == 'systolic':
            diagnosis.append("Possible subaortic or pulmonary stenosis.")
            recommendation.append("Echocardiography recommended for confirmation")
        elif self.location == 'left_apex':
            diagnosis.append("Possible mitral valve degeneration.")
            recommendation.append("Radiography or echocardiography recommended")
        
        return {
            'diagnosis': diagnosis,
            'recommendation': recommendation
        }

    def _check_low_intensity_murmur(self):
        diagnosis = []
        recommendation = []

        if self.clinical_signs == 'none' and self.age_group == 'young':
            diagnosis.append("Functional murmur is possible.")
            recommendation.append("Monitor for progression")
        elif self.location == 'right_base':
            diagnosis.append("Possible tricuspid regurgitation or heartworm infection.")
            recommendation.append("Echocardiography and heartworm antigen test recommended")

        return {
            'diagnosis': diagnosis,
            'recommendation': recommendation
        }

    def action_reset(self):
        self.ensure_one()
        self.write({
            'diagnosis': False,
            'recommendation': False,
            'state': 'draft'
        })
        return True