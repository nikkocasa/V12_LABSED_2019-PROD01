# -*- coding: utf-8 -*-
from odoo import http

# class DbShow(http.Controller):
#     @http.route('/db_show/db_show/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/db_show/db_show/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('db_show.listing', {
#             'root': '/db_show/db_show',
#             'objects': http.request.env['db_show.db_show'].search([]),
#         })

#     @http.route('/db_show/db_show/objects/<model("db_show.db_show"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('db_show.object', {
#             'object': obj
#         })