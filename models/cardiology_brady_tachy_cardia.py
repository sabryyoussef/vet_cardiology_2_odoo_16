from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CardiacAlgorithm(models.Model):
    _name = 'cardiac.algorithm'
    _description = 'Cardiac Diagnostic Algorithm'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Determine the display order"
    )

    # Remove this duplicate definition
    # animal_algorithm_id = fields.Many2one(
    #     'animal.algorithm',
    #     string='Animal Algorithm',
    #     ondelete='cascade'
    # )

    # Keep this one
    animal_algorithm_id = fields.Many2one(
        'animal.algorithm',
        string='Base Algorithm Reference',
        required=True,
        ondelete='cascade',
        tracking=True
    )

    attachment_ids = fields.One2many(
        'ir.attachment', 'res_id', domain=[('res_model', '=', 'cardiac.algorithm')],
        string="Attachments"
    )
    # pdf_filename = fields.Char("PDF Filename")  # Optional, for file name


    # Basic Information
    name = fields.Char(string='Algorithm Name', required=True, tracking=True)

    animal_type = fields.Selection(
        related='animal_algorithm_id.animal_type',
        string='Animal Type',
        store=True
    )

    # Clinical Parameters
    heart_rate = fields.Integer(
        string='Heart Rate (bpm)',
        tracking=True,
        help="Heart rate in beats per minute"
    )
    heart_rate_category = fields.Selection([
        ('brady', 'Bradycardia'),
        ('normal', 'Normal'),
        ('tachy', 'Tachycardia')
    ], compute='_compute_heart_rate_category', store=True)
    rhythm_regular = fields.Boolean(string='Regular Rhythm', tracking=True)
    supraventricular_complexes = fields.Boolean(string='Supraventricular Complexes')

    # ECG Parameters
    ecg_performed = fields.Boolean(string='ECG Performed')
    qrs_duration = fields.Float(string='QRS Duration (sec)')
    p_wave_present = fields.Boolean(string='P Wave Present')
    t_wave_abnormal = fields.Boolean(string='T Wave Abnormal')
    st_segment_abnormal = fields.Boolean(string='ST Segment Abnormal')

    # Clinical Signs
    weakness = fields.Boolean(string='Weakness')
    lethargy = fields.Boolean(string='Lethargy')
    syncope = fields.Boolean(string='Syncope')
    exercise_intolerance = fields.Boolean(string='Exercise Intolerance')
    respiratory_distress = fields.Boolean(string='Respiratory Distress')
    coughing = fields.Boolean(string='Coughing')

    # Diagnostic Results
    diagnosis = fields.Text(string='General Diagnosis', readonly=True)
    treatment_plan = fields.Text(string='Treatment Plan', readonly=True)
    recommendations = fields.Text(string='Recommendations', readonly=True)

    # Tachyarrhythmia Specific Fields
    tachyarrhythmia_diagnosis = fields.Text(string='Tachyarrhythmia Diagnosis', readonly=True)
    tachyarrhythmia_treatment = fields.Text(string='Tachyarrhythmia Treatment', readonly=True)
    tachyarrhythmia_state = fields.Selection([
        ('draft', 'Draft'),
        ('diagnosed', 'Diagnosed')
    ], default='draft', string='Tachyarrhythmia Status')

    # States
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('diagnosed', 'Diagnosed'),
        ('treated', 'Treated'),
        ('resolved', 'Resolved')
    ], default='draft', string='Status', tracking=True)

    @api.depends('heart_rate', 'animal_algorithm_id.animal_type')
    def _compute_heart_rate_category(self):
        for record in self:
            if not record.heart_rate:
                record.heart_rate_category = False
                continue

            if record.animal_algorithm_id.animal_type == 'cat':
                if record.heart_rate < 120:
                    record.heart_rate_category = 'brady'
                elif record.heart_rate > 240:
                    record.heart_rate_category = 'tachy'
                else:
                    record.heart_rate_category = 'normal'
            else:  # dog
                if record.heart_rate < 60:
                    record.heart_rate_category = 'brady'
                elif record.heart_rate > 180:
                    record.heart_rate_category = 'tachy'
                else:
                    record.heart_rate_category = 'normal'

    @api.constrains('heart_rate', 'qrs_duration')
    def _check_values(self):
        for record in self:
            if record.heart_rate and record.heart_rate < 0:
                raise ValidationError("Heart rate cannot be negative")
            if record.qrs_duration and record.qrs_duration < 0:
                raise ValidationError("QRS duration cannot be negative")

    def action_diagnose(self):
        self.ensure_one()
        diagnosis_text = []
        treatment_text = []
        recommendations = []

        # Basic rhythm analysis
        if self.heart_rate_category == 'brady':
            diagnosis_text.append("Bradycardia detected")
            if self.syncope or self.weakness:
                treatment_text.append("Consider temporary pacing")
                recommendations.append("Urgent cardiology consultation recommended")
        elif self.heart_rate_category == 'tachy':
            diagnosis_text.append("Tachycardia detected")
            if self.respiratory_distress:
                treatment_text.append("Oxygen therapy may be needed")
                recommendations.append("Monitor oxygen saturation")

        # ECG analysis
        if self.ecg_performed:
            if not self.p_wave_present:
                diagnosis_text.append("Absent P waves - possible atrial standstill")
            if self.t_wave_abnormal:
                diagnosis_text.append("T wave abnormalities - possible myocardial hypoxia")
            if self.st_segment_abnormal:
                diagnosis_text.append("ST segment abnormalities - possible myocardial injury")

        # Rhythm irregularity analysis
        if not self.rhythm_regular:
            diagnosis_text.append("Irregular rhythm present")
            if self.supraventricular_complexes:
                diagnosis_text.append("Possible atrial fibrillation")
                recommendations.append("ECG monitoring recommended")

        # Clinical signs analysis
        if self.syncope:
            diagnosis_text.append("Syncope present - indicates severe cardiac compromise")
            recommendations.append("Consider Holter monitoring")
        if self.exercise_intolerance:
            diagnosis_text.append("Exercise intolerance indicates reduced cardiac output")
        if self.respiratory_distress:
            diagnosis_text.append("Respiratory distress may indicate congestive heart failure")
            treatment_text.append("Consider diuretic therapy")

        # Update fields
        self.diagnosis = "\n".join(diagnosis_text) if diagnosis_text else "No significant findings"
        self.treatment_plan = "\n".join(treatment_text) if treatment_text else "No immediate treatment required"
        self.recommendations = "\n".join(recommendations) if recommendations else "Regular monitoring advised"
        self.state = 'diagnosed'

        return True

    def manage_tachyarrhythmia(self):
        """Calculate tachyarrhythmia diagnosis based on clinical parameters"""
        self.ensure_one()

        diagnosis_points = []
        treatment_points = []

        # Check heart rate and rhythm
        if self.heart_rate_category == 'tachy':
            diagnosis_points.append("Tachycardia present")

            if not self.rhythm_regular:
                diagnosis_points.append("Irregular rhythm detected")
                if self.supraventricular_complexes:
                    diagnosis_points.append("Supraventricular complexes present")
                    treatment_points.append("Consider anti-arrhythmic medication")
            else:
                diagnosis_points.append("Regular tachycardia")
                treatment_points.append("Monitor for rhythm changes")

        # Check ECG parameters
        if self.ecg_performed:
            if self.qrs_duration > 0.06:
                diagnosis_points.append(f"Prolonged QRS duration: {self.qrs_duration} sec")
                treatment_points.append("ECG monitoring recommended")
            if not self.p_wave_present:
                diagnosis_points.append("Absent P waves")
                treatment_points.append("Consider underlying conduction abnormalities")

        # Check clinical signs
        clinical_signs = []
        if self.weakness:
            clinical_signs.append("weakness")
        if self.lethargy:
            clinical_signs.append("lethargy")
        if self.syncope:
            clinical_signs.append("syncope")
            treatment_points.append("Urgent cardiac evaluation needed")
        if self.exercise_intolerance:
            clinical_signs.append("exercise intolerance")
        if self.respiratory_distress:
            clinical_signs.append("respiratory distress")
            treatment_points.append("Consider oxygen therapy")
        if self.coughing:
            clinical_signs.append("coughing")

        if clinical_signs:
            diagnosis_points.append(f"Clinical signs: {', '.join(clinical_signs)}")

        # Set diagnosis and treatment
        self.tachyarrhythmia_diagnosis = "\n".join(
            diagnosis_points) if diagnosis_points else "No significant tachyarrhythmia findings"
        self.tachyarrhythmia_treatment = "\n".join(treatment_points) if treatment_points else "Continue monitoring"
        self.tachyarrhythmia_state = 'diagnosed'

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Tachyarrhythmia diagnosis calculated successfully',
                'sticky': False,
                'type': 'success',
            }
        }

    def action_clear_diagnosis(self):
        """Clear the tachyarrhythmia diagnosis and reset to draft state"""
        self.ensure_one()
        self.write({
            'tachyarrhythmia_diagnosis': False,
            'tachyarrhythmia_treatment': False,
            'tachyarrhythmia_state': 'draft'
        })
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Tachyarrhythmia diagnosis cleared',
                'sticky': False,
                'type': 'success',
            }
        }

    def action_reset(self):
        self.ensure_one()
        self.write({
            'diagnosis': False,
            'treatment_plan': False,
            'recommendations': False,
            'state': 'draft'
        })
        return True

    def action_set_in_progress(self):
        self.ensure_one()
        self.state = 'in_progress'
        return True

    def action_set_treated(self):
        self.ensure_one()
        self.state = 'treated'
        return True

    def action_set_resolved(self):
        self.ensure_one()
        self.state = 'resolved'
        return True

    # def action_view_pdf(self):
    #     # Generate the URL for the PDF file using the model's `pdf_file` field
    #     return {
    #         'type': 'ir.actions.act_url',
    #         'url': f'/web/content/{self.id}/pdf_file/{self.pdf_filename}',
    #         'target': 'new',  # Opens in a new tab, change to 'self' for popup
    #     }
    def action_view_static_pdf(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/cardiology_sc/static/src/pdf/Vet_Algorithm_Status_Bradycardia_and_Tachycardia.pdf',
            'target': 'new',  # Opens in a new tab or change to 'self' for popup
        }

    def open_image_popup(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'cardiology_sc.image.popup.model',  # Use the correct popup model
            'view_mode': 'form',
            'target': 'new',
            'context': {'image_url': '/cardiology_sc/static/src/img/bradycardia_image.png'},
        }
