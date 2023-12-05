# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Niki Sulotion",
    "summary": """ """,
    "version": "16.0.1.0.0",
    "license": "LGPL-3",
    "author": "",
    "website": "",
    "depends": ["stock","crm","contacts",'sale','purchase'],
    "data": [
            "security/ir.model.access.csv",
             "views/moves_history.xml",
             "views/sale_order.xml",
             "wizard/input_product.xml",
             "views/input_vendor.xml",
             "views/output_vendor.xml",
             "views/document.xml",
             "views/res_oartner_inherit.xml",
             "wizard/output_vendor.xml"
            ],
}
