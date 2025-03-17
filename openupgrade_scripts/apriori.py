""" Encode any known changes to the database here
to help the matching process
"""

# Renamed modules is a mapping from old module name to new module name
renamed_modules = {
    "account_accountant": "accountant",
    # odoo
    # odoo/enterprise
    # OCA/...
}

# Merged modules contain a mapping from old module names to other,
# preexisting module names
merged_modules = {
    # odoo
    # odoo/enterprise
    # OCA/sale-workflow
    "sale_order_qty_change_no_recompute": "sale",
    # OCA/...
}

# only used here for upgrade_analysis
renamed_models = {
    # odoo
    # mail
    "mail.notification.web.push": "web.push",
    "mail.partner.device": "mail.push.device",
    "mail.shortcode": "mail.canned.response",
    # OCA/...
}

# only used here for upgrade_analysis
merged_models = {
    # odoo
    # OCA/...
}
