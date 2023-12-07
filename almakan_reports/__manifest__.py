# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Al Makan Reports',
    'version': '1.0',
    'sequence': -200,
    'category': 'Sales',
    'depends': ['base', 'sale'],
    'data': [
        # 'views/sale_order.xml',
        'report/report_info.xml',
        'report/sale_order_reports.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
