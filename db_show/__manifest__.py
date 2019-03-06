# -*- coding: utf-8 -*-
{
    'name': "db_show",

    'summary': """
        Show curreznt db_name on top left corner""",

    'description': """
        <?xml version="1.0" encoding="utf-8"?>
            <odoo>
                    <template id="contact" inherit_id="web.menu_secondary">
                        <xpath expr="//span[@class='oe_logo_edit']" position="before">
                            <!--<t t-if="True" groups="developer_mode.odoo_developer_group">-->
                                <div style="height:20px;text-align:center;background-color:green;color:#ffffff;">
                                    <t t-esc="request.session.db"/>
                                </div>
                            <!--</t>-->
                        </xpath>
                    </template>
            </odoo>
    """,

    'author': "Nicolas Farrié",
    'website': "http://www.es-natura.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'tool',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/current_db_display.xml',
    ],
}