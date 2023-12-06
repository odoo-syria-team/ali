# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Niki Sulotion",
    "summary": """ """,
    "version": "16.0.1.0.0",
    "license": "LGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "",
    "depends": ["base", "stock", "crm", "contacts", "website", "portal", "web", "purchase", "sale", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/moves_history.xml",
        "views/sale_order.xml",
        "wizard/input_product.xml",
        "views/input_vendor.xml",
        "views/output_vendor.xml",
        "views/document.xml",
        "views/my_account_documents.xml",
        "views/res_oartner_inherit.xml",
        "wizard/output_vendor.xml",
        "views/document_nikki_list_website.xml",
        "views/document_nikki_form_website.xml",
        "views/contact_us_inherit.xml",
        "views/crm_lead.xml",
    ],
    'web.assets_frontend': [
        'niki_sulotion/static/src/js/contact_us_form.js',
    ],
}
