""" Encode any known changes to the database here
to help the matching process
"""

renamed_modules = {
    # OCA/connector
    # Connector module has been unfolded in 2 modules in version 10.0:
    # connector and queue_job. We need to do this to correct upgrade both
    # modules.
    'connector': 'queue_job',
    # OCA/e-commerce
    'website_sale_qty': 'website_sale_price_tier',
    # OCA/hr
    # The OCA extensions of the hr_holidays module are 'hr_holidays_something'
    'hr_holiday_notify_employee_manager':
        'hr_holidays_notify_employee_manager',
    # OCA/manufacture-reporting:
    'report_mrp_bom_matrix': 'mrp_bom_matrix_report',
    # OCA/sale-workflow:
    'sale_delivery_block': 'sale_stock_picking_blocking',
    # OCA/server-tools:
    'mail_log_messages_to_process': 'mail_log_message_to_process',
    # Akretion section : Use with merge
    'account_invoice_product_supplier_price_update':
        'account_invoice_supplierinfo_update',
    'web_sheet_full_width_selective': 'web_sheet_full_width',
    'sale_payment_method_automatic_workflow':
        'sale_automatic_workflow_payment_mode',
}

renamed_models = {
}
