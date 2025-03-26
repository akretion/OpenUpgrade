""" Encode any known changes to the database here
to help the matching process
"""

# Renamed modules is a mapping from old module name to new module name
renamed_modules = {
    # odoo
    "l10n_es_pos_tbai": "l10n_es_edi_tbai_pos",
    "mrp_subonctracting_landed_costs": "mrp_subcontracting_landed_costs",
    "website_sale_picking": "website_sale_collect",
    "website_form_project": "website_project",
    # odoo/enterprise
    # OCA/...
}

# Merged modules contain a mapping from old module names to other,
# preexisting module names
merged_modules = {
    # odoo
    "account_audit_trail": "account",
    "account_lock": "account",
    "account_payment_term": "account",
    "l10n_br_pix": "l10n_br",
    "l10n_de_audit_trail": "l10n_de",
    "l10n_dk_audit_trail": "l10n_dk",
    "l10n_dk_bookkeeping": "account",
    "l10n_es_edi_facturae_adm_centers": "l10n_es_edi_facturae",
    "l10n_es_edi_facturae_invoice_period": "l10n_es_edi_facturae",
    "l10n_es_edi_tbai_multi_refund": "l10n_es_edi_tbai",
    "l10n_fr_fec": "l10n_fr",
    "l10n_fr_invoice_addr": "l10n_fr_account",
    "l10n_ro_efactura": "l10n_ro_edi",
    "im_livechat_mail_bot": "mail_bot",
    "payment_ogone": "payment_worldline",
    "payment_sips": "payment_worldline",
    "pos_sale_product_configurator": "pos_sale",
    "sale_product_configurator": "sale",
    "spreadsheet_dashboard_purchase": "spreadsheet_dashboard_purchase_stock",
    "stock_landed_costs_company": "stock_landed_costs",
    "website_sale_product_configurator": "website_sale",
    # odoo/enterprise
    # OCA/l10n-france
    "l10n_fr_pos_cert_update_draft_order_line": "l10n_fr_pos_cert",
    # OCA/sale-workflow
    "sale_order_qty_change_no_recompute": "sale",
    # OCA/...
}

# only used here for upgrade_analysis
renamed_models = {
    # odoo
    "l10n_es_edi_facturae_adm_centers.ac_role_type": ""
    "l10n_es_edi_facturae.ac_role_type",
    "mail.notification.web.push": "web.push",
    "mail.partner.device": "mail.push.device",
    "mail.shortcode": "mail.canned.response",
    "pos.combo": "product.combo",
    "pos.combo.line": "product.combo.item",
    # OCA/...
}

# only used here for upgrade_analysis
merged_models = {
    # odoo
    # OCA/...
}
