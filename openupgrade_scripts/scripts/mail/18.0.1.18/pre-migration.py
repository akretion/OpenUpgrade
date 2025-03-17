# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

model_renames = [
    ("mail.notification.web.push", "web.push"),
    ("mail.partner.device", "mail.push.device"),
    ("mail.shortcode", "mail.canned.response"),
]

table_renames = [
    ("mail_notification_web_push", "web_push"),
    ("mail_partner_device", "mail_push_device"),
    ("mail_shortcode", "mail_canned_response"),
]

field_renames = [
    ("web.push", "web_push", "user_device", "mail_push_device_id"),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_models(env.cr, model_renames)
    openupgrade.rename_tables(env.cr, table_renames)
    openupgrade.rename_fields(env, field_renames)
