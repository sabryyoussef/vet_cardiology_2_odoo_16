from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CatHeartMurmur(models.Model):
    _name = 'veterinary.cat.heart.murmur'
    _description = 'Cat Heart Murmur Diagnosis'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _rec_name = 'cat_name'

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
        domain="[('animal_type', '=', 'cat')]"  # Only show cat algorithms
    )
    # Add related field for animal type
    animal_type = fields.Selection(
        related='animal_algorithm_id.animal_type',
        string='Animal Type',
        store=True
    )

    # Basic Information
    cat_name = fields.Char(string='Cat Name', required=True)
    age = fields.Float(string='Age (Years)', required=True)
    murmur_grade = fields.Selection([
        ('1', 'Grade I'),
        ('2', 'Grade II'),
        ('3', 'Grade III'),
        ('4', 'Grade IV'),
        ('5', 'Grade V'),
        ('6', 'Grade VI'),
        ('continuous', 'Continuous'),
    ], string='Murmur Grade', required=True)
    
    # Clinical Parameters
    pcv = fields.Float(string='Packed Cell Volume (%)', required=True)
    nt_pro_bnp = fields.Float(string='NT-proBNP (pmol/L)', required=True)
    t4_level = fields.Selection([
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High')
    ], string='T4 Level', required=True)
    has_fever = fields.Boolean(string='Has Fever/Infection')

    # Diagnosis Results
    anemia_result = fields.Text(string='Anemia Check Result', readonly=True)
    murmur_result = fields.Text(string='Murmur Diagnosis Result', readonly=True)
    thyroid_result = fields.Text(string='Thyroid Check Result', readonly=True)
    age_evaluation_result = fields.Text(string='Age Evaluation Result', readonly=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('diagnosed', 'Diagnosed')
    ], default='draft', string='Status')

    @api.constrains('age', 'pcv', 'nt_pro_bnp')
    def _check_values(self):
        for record in self:
            if record.age < 0:
                raise ValidationError("Age cannot be negative")
            if record.pcv < 0 or record.pcv > 100:
                raise ValidationError("PCV must be between 0 and 100")
            if record.nt_pro_bnp < 0:
                raise ValidationError("NT-proBNP cannot be negative")

    def check_anemia(self):
        self.ensure_one()
        if self.pcv < 28:
            return "Anemia: Correct anemia, investigate causes, recheck murmur after normalization."
        return "No significant anemia."

    def diagnose_murmur(self):
        self.ensure_one()
        murmur_grade = int(self.murmur_grade) if self.murmur_grade != 'continuous' else 'continuous'
        
        if isinstance(murmur_grade, int) and murmur_grade >= 4:
            return "Congenital heart disease likely. Consider echocardiogram."
        elif murmur_grade == "continuous":
            return "Patent ductus arteriosus likely. Confirm with echocardiogram."
        else:
            if self.nt_pro_bnp < 100:
                return "Physiologic cause likely; heart disease less likely."
            return "Heart disease more likely; confirm with echocardiogram."

    def check_thyroid(self):
        self.ensure_one()
        if self.t4_level == 'high':
            return "Hyperthyroid: Treat and reassess murmur after establishing euthyroidism."
        return "Thyroid status normal."

    def evaluate_age_related_disease(self):
        self.ensure_one()
        if self.age < 1:
            return "Young cat: Likely physiologic murmur."
        elif 1 <= self.age < 7:
            return "Adult cat: Consider congenital heart disease if murmur grade is high."
        return "Older cat: Suspect organic heart disease, consider hypertrophic cardiomyopathy."

    def action_diagnose(self):
        self.ensure_one()
        self.anemia_result = self.check_anemia()
        self.murmur_result = self.diagnose_murmur()
        self.thyroid_result = self.check_thyroid()
        self.age_evaluation_result = self.evaluate_age_related_disease()
        self.state = 'diagnosed'
        return True

    def action_reset(self):
        self.ensure_one()
        self.write({
            'anemia_result': False,
            'murmur_result': False,
            'thyroid_result': False,
            'age_evaluation_result': False,
            'state': 'draft'
        })
        return True