from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError
from odoo.tools import float_compare

class AnimalAlgorithm(models.Model):
    _name = 'animal.algorithm'
    _description = 'Animal Algorithm'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'priority desc, sequence, id desc'

    # Basic Information
    name = fields.Char(
        string='Name',
        required=True,
        tracking=True,
        index=True,
        translate=True,
        help="Name of the algorithm"
    )

    sequence = fields.Char(
        string='Reference',
        required=True,
        readonly=True,
        default='New',
        copy=False,
        tracking=True,
        index=True,
        help="Unique identifier for this algorithm"
    )

    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'High'),
    ], default='0', string='Priority', index=True)

    animal_type = fields.Selection([
        ('cat', 'Cat'),
        ('dog', 'Dog')
    ], string='Animal Type',
        required=True,
        tracking=True,
        default='cat',
        index=True
    )

    description = fields.Text(
        string='Description',
        tracking=True,
        translate=True,
        sanitize=True,
        strip_style=True,
        help="Detailed description of the algorithm"
    )

    notes = fields.Text(
        string='Notes',
        tracking=True,
        translate=True,
        sanitize=True,
        strip_style=True,
        help="Additional notes and observations"
    )

    # Company and Access Fields
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        index=True
    )

    user_id = fields.Many2one(
        'res.users',
        string='Responsible',
        default=lambda self: self.env.user,
        tracking=True,
        index=True
    )

    # Status Fields
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('validated', 'Validated'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status',
        default='draft',
        tracking=True,
        required=True,
        copy=False,
        group_expand='_expand_states'
    )

    active = fields.Boolean(
        default=True,
        tracking=True,
        help="If unchecked, it will allow you to hide the algorithm without removing it."
    )

    # Relationships
    cat_heart_murmur_ids = fields.One2many(
        'veterinary.cat.heart.murmur',
        'animal_algorithm_id',
        string='Cat Heart Murmur Diagnoses',
        domain=[('animal_type', '=', 'cat')],
        copy=True
    )

    dog_heart_murmur_ids = fields.One2many(
        'veterinary.dog.heart.murmur',
        'animal_algorithm_id',
        string='Dog Heart Murmur Diagnoses',
        domain=[('animal_type', '=', 'dog')],
        copy=True
    )

    pulse_alteration_ids = fields.One2many(
        'veterinary.pulse.alteration',
        'animal_algorithm_id',
        string='Pulse Alterations',
        copy=True
    )

    tachyarrhythmia_ids = fields.One2many(
        'veterinary.tachyarrhythmia',
        'animal_algorithm_id',
        string='Tachyarrhythmias'
    )

    # Computed Fields
    heart_murmur_count = fields.Integer(
        string='Heart Murmurs',
        compute='_compute_heart_murmur_count',
        store=True,
        help="Total number of heart murmurs",
        search='_search_heart_murmur_count'
    )

    last_activity_date = fields.Datetime(
        string='Last Activity',
        compute='_compute_last_activity',
        store=True,
        index=True
    )

    # Compute Methods
    @api.depends_context('company_id')
    @api.depends('cat_heart_murmur_ids', 'dog_heart_murmur_ids')
    def _compute_heart_murmur_count(self):
        for record in self:
            record.heart_murmur_count = len(record.cat_heart_murmur_ids) + len(record.dog_heart_murmur_ids)

    @api.depends('message_ids', 'activity_ids')
    def _compute_last_activity(self):
        for record in self:
            dates = []
            if record.message_ids:
                dates.append(max(record.message_ids.mapped('date')))
            if record.activity_ids:
                dates.append(max(record.activity_ids.mapped('create_date')))
            record.last_activity_date = max(dates) if dates else False

    # Search Methods
    @api.model
    def _search_heart_murmur_count(self, operator, value):
        algorithms = self.search([]).filtered(
            lambda x: float_compare(x.heart_murmur_count, value, precision_digits=0) == 0
        )
        return [('id', 'in', algorithms.ids)]

    # CRUD Methods
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sequence', 'New') == 'New':
                vals['sequence'] = self.env['ir.sequence'].next_by_code('animal.algorithm') or 'New'
        return super().create(vals_list)

    def write(self, vals):
        # Track significant changes
        if 'state' in vals:
            self.message_post(
                body=_("State changed to: %s") % dict(self._fields['state'].selection).get(vals['state'])
            )
        return super().write(vals)

    def unlink(self):
        for record in self:
            if record.state not in ('draft', 'cancelled'):
                raise ValidationError(_("You can only delete algorithms in 'Draft' or 'Cancelled' state."))
        return super().unlink()

    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        default.update({
            'sequence': 'New',
            'state': 'draft',
            'name': _("%s (Copy)") % self.name,
            'active': True,
        })
        return super().copy(default)

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults.update({
            'company_id': self.env.company.id,
            'user_id': self.env.user.id,
        })
        return defaults

    # Name Methods
    def name_get(self):
        result = []
        for record in self:
            priority_star = '⭐ ' if record.priority == '1' else ''
            name = f'{priority_star}[{record.sequence}] {record.name}'
            result.append((record.id, name))
        return result

    # Onchange Methods
    @api.onchange('animal_type')
    def _onchange_animal_type(self):
        if self.animal_type == 'cat':
            self.dog_heart_murmur_ids = False
        elif self.animal_type == 'dog':
            self.cat_heart_murmur_ids = False

    # State Management Methods
    def action_set_draft(self):
        self._check_state_access('draft')
        return self.write({'state': 'draft', 'active': True})

    def action_set_in_progress(self):
        self._check_state_access('in_progress')
        return self.write({'state': 'in_progress'})

    def action_validate(self):
        self._check_state_access('validated')
        return self.write({'state': 'validated'})

    def action_set_done(self):
        self._check_state_access('done')
        return self.write({'state': 'done'})

    def action_cancel(self):
        self._check_state_access('cancelled')
        return self.write({
            'state': 'cancelled',
            'active': False
        })

    def _check_state_access(self, new_state):
        """Check access rights for state changes"""
        self.ensure_one()
        if new_state in ['validated', 'done'] and not self.env.user.has_group('cardiology_sc.group_veterinary_manager'):
            raise AccessError(_("Only veterinary managers can validate or complete algorithms."))

    # Activity Management
    def action_schedule_meeting(self):
        """Schedule a meeting related to this algorithm"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Schedule Meeting'),
            'res_model': 'calendar.event',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_res_id': self.id,
                'default_res_model': self._name,
                'default_name': _("Review: %s") % self.name,
                'default_partner_ids': [(4, self.user_id.partner_id.id)],
            }
        }

    # Batch Processing Methods
    def action_mass_validate(self):
        """Validate multiple algorithms at once"""
        if not self.env.user.has_group('cardiology_sc.group_veterinary_manager'):
            raise AccessError(_("Only veterinary managers can perform mass validation."))
        return self.filtered(lambda r: r.state == 'in_progress').write({'state': 'validated'})

    # Utility Methods
    @api.model
    def _expand_states(self, states, domain, order):
        return [key for key, val in self._fields['state'].selection]

    # Constraints
    _sql_constraints = [
        ('name_uniq', 'unique(name, company_id)', _('Algorithm name must be unique per company!')),
        ('sequence_uniq', 'unique(sequence)', _('Algorithm reference must be unique!')),
    ]

    @api.constrains('state')
    def _check_state_constraints(self):
        for record in self:
            if record.state == 'validated' and not record.description:
                raise ValidationError(_("Description is required before validating the algorithm."))
            elif record.state == 'done' and not (
                record.cat_heart_murmur_ids or
                record.dog_heart_murmur_ids or
                record.pulse_alteration_ids
            ):
                raise ValidationError(_("At least one related record is required before marking as done."))

    @api.constrains('animal_type')
    def _check_animal_type_consistency(self):
        for record in self:
            if record.animal_type == 'cat' and record.dog_heart_murmur_ids:
                raise ValidationError(_("Cannot change to Cat type when Dog Heart Murmurs exist."))
            if record.animal_type == 'dog' and record.cat_heart_murmur_ids:
                raise ValidationError(_("Cannot change to Dog type when Cat Heart Murmurs exist."))

    # Add these methods to your AnimalAlgorithm class

    # def action_view_cardiac_algorithms(self):
    #     self.ensure_one()
    #     return {
    #         'name': _('Cardiac Algorithms'),
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'cardiac.algorithm',
    #         'view_mode': 'tree,form',
    #         'domain': [('animal_algorithm_id', '=', self.id)],
    #         'context': {
    #             'default_animal_algorithm_id': self.id,
    #             'default_animal_type': self.animal_type,
    #         },
    #     }

    def action_view_heart_murmurs(self):
        self.ensure_one()
        if self.animal_type == 'cat':
            return {
                'name': _('Cat Heart Murmurs'),
                'type': 'ir.actions.act_window',
                'res_model': 'veterinary.cat.heart.murmur',
                'view_mode': 'tree,form',
                'domain': [('animal_algorithm_id', '=', self.id)],
                'context': {
                    'default_animal_algorithm_id': self.id,
                    'default_animal_type': 'cat',
                },
            }
        else:
            return {
                'name': _('Dog Heart Murmurs'),
                'type': 'ir.actions.act_window',
                'res_model': 'veterinary.dog.heart.murmur',
                'view_mode': 'tree,form',
                'domain': [('animal_algorithm_id', '=', self.id)],
                'context': {
                    'default_animal_algorithm_id': self.id,
                    'default_animal_type': 'dog',
                },
            }

    def action_view_pulse_alterations(self):
        self.ensure_one()
        return {
            'name': _('Pulse Alterations'),
            'type': 'ir.actions.act_window',
            'res_model': 'veterinary.pulse.alteration',
            'view_mode': 'tree,form',
            'domain': [('animal_algorithm_id', '=', self.id)],
            'context': {
                'default_animal_algorithm_id': self.id,
                'default_animal_type': self.animal_type,
            },
        }

    cardiac_algorithm_ids = fields.One2many(
        'cardiac.algorithm',
        'animal_algorithm_id',
        string='Cardiac Algorithms'
    )