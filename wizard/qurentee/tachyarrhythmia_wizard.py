from odoo import models, fields, api

class TachyarrhythmiaWizard(models.TransientModel):
    _name = 'tachyarrhythmia.wizard'
    _description = 'Tachyarrhythmia Management Wizard'

    state = fields.Selection([
        ('species', 'Species Selection'),
        ('rhythm', 'Rhythm Assessment'),
        ('complexes', 'QRS Complexes'),
        ('treatment', 'Treatment Plan')
    ], default='species', string='Status', required=True)
    
    species = fields.Selection([
        ('canine', 'Canine'),
        ('feline', 'Feline')
    ], string='Species')
    
    rhythm = fields.Selection([
        ('regular', 'Regular'),
        ('irregular', 'Irregular')
    ], string='Rhythm')
    
    complexes = fields.Selection([
        ('narrow', 'Narrow'),
        ('wide', 'Wide')
    ], string='QRS Complexes')

    diagnosis = fields.Text(string='Diagnosis')
    treatment_plan = fields.Text(string='Treatment Plan')

    @api.onchange('rhythm', 'complexes')
    def _onchange_diagnosis(self):
        if not self.rhythm:
            return

        if self.rhythm == 'irregular':
            self.diagnosis = 'Atrial Fibrillation'
            self.treatment_plan = '''
- Decrease heart rate with agents (digoxin, calcium-channel blockers, β-blockers)
- Consider rhythm control with transthoracic electric cardioversion
            '''
        elif self.rhythm == 'regular':
            if self.complexes == 'narrow':
                self.diagnosis = 'Sustained SVT or Paroxysmal SVT'
                self.treatment_plan = '''
- Perform vagal maneuvers (carotid sinus massage, ocular pressure, precordial thump)
- Administer IV boluses of procainamide, diltiazem, or esmolol
- Consider transthoracic electrical cardioversion
                '''
            elif self.complexes == 'wide':
                self.diagnosis = 'Ventricular Tachycardia'
                self.treatment_plan = '''
- If VT is rapid or symptomatic, administer IV lidocaine or procainamide
- Identify and treat underlying heart disease and correct electrolyte imbalances
- Withdraw any potentially offending drugs
- Consider sotalol or mexiletine for long-term maintenance
                '''
            elif self.complexes == 'undetermined':
                self.diagnosis = 'Sinus Tachycardia'
                self.treatment_plan = '- Treat underlying causes'

    def action_previous(self):
        states = ['species', 'rhythm', 'complexes', 'treatment']
        current_index = states.index(self.state)
        if current_index > 0:
            self.state = states[current_index - 1]
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def action_next(self):
        states = ['species', 'rhythm', 'complexes', 'treatment']
        current_index = states.index(self.state)
        if current_index < len(states) - 1:
            self.state = states[current_index + 1]
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def action_back(self):
        if self.state == 'rhythm':
            self.state = 'species'
        elif self.state == 'complexes':
            self.state = 'rhythm'
        elif self.state == 'treatment':
            if self.rhythm == 'irregular':
                self.state = 'rhythm'
            else:
                self.state = 'complexes'
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
    # ... existing imports and code ...

    @api.onchange('state')
    def _onchange_state(self):
        if self.state == 'treatment':
            self._compute_diagnosis_and_treatment()

    def _compute_diagnosis_and_treatment(self):
        # Start with species-specific base diagnosis
        diagnosis_parts = []
        treatment_parts = []
        
        # Add species
        if self.species == 'canine':
            diagnosis_parts.append("Canine patient")
        else:
            diagnosis_parts.append("Feline patient")
            
        # Add rhythm assessment
        if self.rhythm == 'regular':
            diagnosis_parts.append("with regular rhythm")
        else:
            diagnosis_parts.append("with irregular rhythm")
            
        # Add complex assessment
        if self.complexes == 'narrow':
            diagnosis_parts.append("and narrow QRS complexes")
        else:
            diagnosis_parts.append("and wide QRS complexes")
            
        # Compile final diagnosis
        self.diagnosis = " ".join(diagnosis_parts)
        
        # Determine treatment based on conditions
        if self.species == 'canine':
            if self.rhythm == 'regular':
                if self.complexes == 'narrow':
                    treatment_parts.append("- Consider vagal maneuvers\n")
                    treatment_parts.append("- If unsuccessful, administer Adenosine\n")
                    treatment_parts.append("- Monitor cardiac response\n")
                else:  # wide complexes
                    treatment_parts.append("- Administer Lidocaine\n")
                    treatment_parts.append("- Monitor cardiac response\n")
                    treatment_parts.append("- Consider cardioversion if unstable\n")
            else:  # irregular
                treatment_parts.append("- Evaluate for atrial fibrillation\n")
                treatment_parts.append("- Consider rate control medications\n")
                treatment_parts.append("- Monitor cardiac status\n")
        else:  # feline
            if self.rhythm == 'regular':
                if self.complexes == 'narrow':
                    treatment_parts.append("- Consider beta blockers\n")
                    treatment_parts.append("- Monitor cardiac response\n")
                else:  # wide complexes
                    treatment_parts.append("- Evaluate for structural heart disease\n")
                    treatment_parts.append("- Consider antiarrhythmic medication\n")
            else:  # irregular
                treatment_parts.append("- Evaluate for underlying cardiac disease\n")
                treatment_parts.append("- Consider rate control\n")
                treatment_parts.append("- Monitor closely\n")
        
        self.treatment_plan = "".join(treatment_parts)