from odoo import models, fields

class ImagePopupModel(models.TransientModel):
    _name = 'cardiology_sc.image.popup.model'  # Use underscores as per Odoo conventions
    _description = 'Image Popup Model'


    image_url = fields.Char(string="Image URL")

    def open_image_in_new_window(self):
        self.image_url = 'http://localhost:8016/cardiology_sc/static/img/bradycardia_image.png'
        return {
            'type': 'ir.actions.act_url',
            'url': self.image_url,
            'target': 'new',  # This will open the link in a new window
        }

    # def open_image_popup(self):
    #     self.image_url = 'http://localhost:8016/cardiology_sc/static/img/bradycardia_image.png'
    #     print("Opening popup with URL:", self.image_url)  # Debug statement
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'cardiology_sc.image.popup.model',
    #         'view_mode': 'form',
    #         'target': 'new',
    #     }

    # def open_image_popup(self):
    #     self.image_url = 'http://localhost:8016/cardiology_sc/static/img/bradycardia_image.png'
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'cardiology_sc.image.popup.model',  # Correct the res_model reference
    #         'view_mode': 'form',
    #         'target': 'new',
    #         'context': {'image_url': '/cardiology_sc/static/src/img/bradycardia_image.png'},  # Set image URL in context
    #     }

    def action_close(self):
        return {'type': 'ir.actions.act_window_close'}
