# /home/user2/odoo16/odoo16/custom_addons/your_module/models/vet_chapter.py
from odoo import models, fields


class VetChapter(models.Model):
    _name = 'vet.chapter'
    _description = 'Vet Chapter'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
