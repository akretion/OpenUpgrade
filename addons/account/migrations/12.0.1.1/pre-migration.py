# Copyright 2018 Eficent <http://www.eficent.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade

column_copies = {
    'account_payment_term_line': [
        ('option', None, None),
    ],
}

_column_renames = {
    'account_tax': [
        ('tax_adjustment', None),
    ],
    'account_tax_template': [
        ('tax_adjustment', None),
        ('cash_basis_account', 'cash_basis_account_id'),
    ],
    'account_chart_template': [
        ('company_id', None),
    ],
    'account_invoice': [
        ('reference_type', None),
    ],
#    'account_invoice_line': [
#        ('layout_category_id', None),
#    ],
}

#_table_renames = [
#    ('stock_incoterms', 'account_incoterms')
#]

#_model_renames = [
#    ('stock.incoterms', 'account.incoterms')
#]

_field_renames = [
    ('res.config.settings', 'res_config_settings', 'group_show_price_subtotal',
     'group_show_line_subtotals_tax_excluded'),
    ('res.config.settings', 'res_config_settings', 'group_show_price_total',
     'group_show_line_subtotals_tax_included'),
#    ('res.config.settings', 'res_config_settings', 'sale_show_tax',
#     'show_line_subtotals_tax_selection'),
]

xmlid_renames = [
    ('sale.group_show_price_subtotal',
     'account.group_show_line_subtotals_tax_excluded'),
    ('sale.group_show_price_total',
     'account.group_show_line_subtotals_tax_included'),
]


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    cr = env.cr
#    openupgrade.rename_tables(cr, _table_renames)
#    openupgrade.rename_models(cr, _model_renames)
    openupgrade.copy_columns(cr, column_copies)
    openupgrade.rename_columns(cr, _column_renames)
#    openupgrade.rename_xmlids(cr, xmlid_renames)
    openupgrade.rename_fields(env, _field_renames)
