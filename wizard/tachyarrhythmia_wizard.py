from odoo import models, fields, api

class TachyarrhythmiaWizard(models.TransientModel):
    _name = 'tachyarrhythmia.wizard'
    _description = 'Tachyarrhythmia Management Wizard'

    # Wizard State Management
    state = fields.Selection([
        ('species', 'Species Selection'),
        ('heart_rate', 'Heart Rate'),
        ('rhythm', 'Rhythm Assessment'),
        ('complexes', 'QRS Complexes'),
        ('clinical', 'Clinical Signs'),
        ('diagnosis', 'Diagnosis')
    ], default='species', string='Status', required=True)
    
    # Step 1: Species Selection
    species = fields.Selection([
        ('canine', 'Canine'),
        ('feline', 'Feline')
    ], string='Species')
    
    # Step 2: Heart Rate
    heart_rate = fields.Integer(string='Heart Rate (bpm)')
    is_tachycardic = fields.Boolean(string='Tachycardic', compute='_compute_tachycardia')
    
    # Step 3: Rhythm Assessment
    rhythm = fields.Selection([
        ('regular', 'Regular'),
        ('irregular', 'Irregular')
    ], string='Rhythm')
    pulse_deficit = fields.Boolean(string='Pulse Deficit Present')
    
    # Step 4: QRS Complexes
    complexes = fields.Selection([
        ('narrow', 'Narrow'),
        ('wide', 'Wide')
    ], string='QRS Complexes')
    p_waves = fields.Selection([
        ('normal', 'Normal'),
        ('absent', 'Absent'),
        ('abnormal', 'Abnormal')
    ], string='P Waves')

    # Step 5: Clinical Signs
    syncope = fields.Boolean(string='Syncope')
    weakness = fields.Boolean(string='Weakness')
    collapse = fields.Boolean(string='Collapse')
    
    # Results
    diagnosis = fields.Text(string='Diagnosis', readonly=True)
    treatment_plan = fields.Text(string='Treatment Plan', readonly=True)
    risk_level = fields.Selection([
        ('low', 'Low Risk'),
        ('moderate', 'Moderate Risk'),
        ('high', 'High Risk'),
        ('critical', 'Critical')
    ], string='Risk Level', readonly=True)

    @api.depends('species', 'heart_rate')
    def _compute_tachycardia(self):
        for record in self:
            if record.species and record.heart_rate:
                threshold = 160 if record.species == 'canine' else 220
                record.is_tachycardic = record.heart_rate > threshold
            else:
                record.is_tachycardic = False

    @api.onchange('state')
    def _onchange_state(self):
        if self.state == 'diagnosis':
            self._compute_diagnosis()

    def _compute_diagnosis(self):
        self.ensure_one()
        
        # Initialize diagnosis components
        diagnosis = []
        treatment = []
        risk = 'low'

        # Scenario 1: Atrial Fibrillation
        if self.rhythm == 'irregular' and self.p_waves == 'absent':
            diagnosis.append("Atrial Fibrillation")
            treatment.extend([
                "1. Rate control with:",
                "   - Digoxin",
                "   - β-blockers",
                "   - Calcium channel blockers",
                "2. Consider anticoagulation",
                "3. Evaluate for underlying cardiac disease"
            ])
            risk = 'high' if self.syncope or self.collapse else 'moderate'

        # Scenario 2: SVT
        elif self.rhythm == 'regular' and self.complexes == 'narrow':
            diagnosis.append("Supraventricular Tachycardia (SVT)")
            treatment.extend([
                "1. Vagal maneuvers",
                "2. If unsuccessful:",
                "   - IV Adenosine",
                "   - IV Diltiazem",
                "3. Consider cardioversion if unstable"
            ])
            risk = 'moderate'

        # Scenario 3: VT
        elif self.complexes == 'wide':
            diagnosis.append("Ventricular Tachycardia")
            treatment.extend([
                "IMMEDIATE TREATMENT:",
                "1. IV Lidocaine or Procainamide",
                "2. Immediate cardioversion if unstable",
                "3. Correct electrolyte imbalances",
                "4. Long-term management plan"
            ])
            risk = 'critical'

        # Set the computed values
        self.diagnosis = "\n".join(diagnosis)
        self.treatment_plan = "\n".join(treatment)
        self.risk_level = risk

    def action_next(self):
        # Validate current state
        if self.state == 'species' and not self.species:
            raise models.ValidationError('Please select a species before continuing.')
        elif self.state == 'heart_rate' and not self.heart_rate:
            raise models.ValidationError('Please enter the heart rate before continuing.')
        elif self.state == 'rhythm' and not self.rhythm:
            raise models.ValidationError('Please select the rhythm before continuing.')
        elif self.state == 'complexes' and not self.complexes:
            raise models.ValidationError('Please select the QRS complex type before continuing.')

        # Progress to next state
        states = ['species', 'heart_rate', 'rhythm', 'complexes', 'clinical', 'diagnosis']
        current_index = states.index(self.state)
        if current_index < len(states) - 1:
            self.state = states[current_index + 1]
            # If moving to diagnosis, compute it
            if self.state == 'diagnosis':
                self._compute_diagnosis()

        return self._return_wizard_action()

    def action_previous(self):
        states = ['species', 'heart_rate', 'rhythm', 'complexes', 'clinical', 'diagnosis']
        current_index = states.index(self.state)
        if current_index > 0:
            self.state = states[current_index - 1]
        return self._return_wizard_action()

    def _return_wizard_action(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }