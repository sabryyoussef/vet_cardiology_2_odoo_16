# -*- coding: utf-8 -*-
# from odoo import http


# class CardiologySc(http.Controller):
#     @http.route('/cardiology_sc/cardiology_sc', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cardiology_sc/cardiology_sc/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cardiology_sc.listing', {
#             'root': '/cardiology_sc/cardiology_sc',
#             'objects': http.request.env['cardiology_sc.cardiology_sc'].search([]),
#         })

#     @http.route('/cardiology_sc/cardiology_sc/objects/<model("cardiology_sc.cardiology_sc"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cardiology_sc.object', {
#             'object': obj
#         })
