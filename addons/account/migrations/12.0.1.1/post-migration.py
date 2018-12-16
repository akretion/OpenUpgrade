# Copyright 2018 Eficent <http://www.eficent.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade
from psycopg2.extensions import AsIs


def map_account_payment_term_line_option(cr):
    openupgrade.map_values(
        cr,
        openupgrade.get_legacy_name('option'),
        'option',
        [('fix_day_following_month', 'after_invoice_month'),
         ('last_day_following_month', 'day_following_month'),
         ('last_day_current_month', 'day_current_month'),
         ],
        table='account_payment_term_line', write='sql')


def map_account_tax_type_tax_use(cr):
    cr.execute(
        """
        UPDATE account_tax
        SET type_tax_use = 'adjustment'
        WHERE type_tax_use = 'none' AND %s = TRUE
        """, (AsIs(openupgrade.get_legacy_name('tax_adjustment')), ),
    )
    cr.execute(
        """
        UPDATE account_tax_template
        SET type_tax_use = 'adjustment'
        WHERE type_tax_use = 'none' AND %s = TRUE
        """, (AsIs(openupgrade.get_legacy_name('tax_adjustment')), ),
    )


def fill_bank_statement_line_account_number(cr):
    cr.execute(
        """
        UPDATE account_bank_statement_line absl
        SET account_number = rpb.acc_number
        FROM res_partner_bank rpb
        WHERE absl.bank_account_id = rpb.id AND rpb.acc_number IS NOT NULL
        """
    )


def fill_account_chart_template_account_code_prefix(cr):
    cr.execute(
        """
        UPDATE account_chart_template act
        SET bank_account_code_prefix = rc.bank_account_code_prefix
        FROM res_company rc
        WHERE act.%s = rc.id AND act.bank_account_code_prefix IS NULL
        """, (AsIs(openupgrade.get_legacy_name('company_id')), ),
    )
    cr.execute(
        """
        UPDATE account_chart_template act
        SET cash_account_code_prefix = rc.cash_account_code_prefix
        FROM res_company rc
        WHERE act.%s = rc.id AND act.cash_account_code_prefix IS NULL
        """, (AsIs(openupgrade.get_legacy_name('company_id')), ),
    )
    # we can't use here new transfer_account_code_prefix field of res_company:
    cr.execute(
        """
        UPDATE account_chart_template act
        SET transfer_account_code_prefix = aa.code
        FROM res_company rc
        LEFT JOIN account_account aa ON rc.transfer_account_id = aa.id
        WHERE act.%s = rc.id
        """, (AsIs(openupgrade.get_legacy_name('company_id')), ),
    )


def fill_account_payment_partner_bank_account_id(cr):
    cr.execute(
        """
        UPDATE account_payment ap
        SET partner_bank_account_id = COALESCE(rp_rpb_rel.rpb, rp_rpb_rel2.rpb)
        FROM res_partner rp
        LEFT JOIN (
            SELECT min(rpb.id) as rpb, rp.id
            FROM res_partner rp
            INNER JOIN res_partner_bank rpb ON rpb.partner_id = rp.id
            GROUP BY rp.id
            ) rp_rpb_rel ON rp_rpb_rel.id = rp.id
        LEFT JOIN res_partner rp2 ON rp.commercial_partner_id = rp2.id
        LEFT JOIN (
            SELECT min(rpb.id) as rpb, rp.id
            FROM res_partner rp
            INNER JOIN res_partner_bank rpb ON rpb.partner_id = rp.id
            GROUP BY rp.id
            ) rp_rpb_rel2 ON rp_rpb_rel2.id = rp2.id
        WHERE rp.id = ap.partner_id 
        """
    )


def fill_account_journal_alias_id(env):
    cr = env.cr
    cr.execute(
        """
        SELECT id
        FROM account_journal
        WHERE type = 'purchase'
        """
    )
    journal_model = env["account.journal"]
    journals = journal_model.browse(cr.fetchone())
    for journal in journals:
        journal._update_mail_alias({})


def fill_account_invoice_line_display_type(cr):
    cr.execute(
        """
        UPDATE account_invoice_line
        SET display_type = 'line_section'
        WHERE %s = IS NOT NULL
        """, (AsIs(openupgrade.get_legacy_name('layout_category_id')), ),
    )


def update_res_company_account_setup_steps_states(cr):
    cr.execute(
        """
        UPDATE res_company
        SET account_setup_bank_data_state = 'done'
        WHERE account_setup_bank_data_done = TRUE
        """
    )
    cr.execute(
        """
        UPDATE res_company
        SET account_setup_fy_data_state = 'done'
        WHERE account_setup_fy_data_done = TRUE
        """
    )
    cr.execute(
        """
        UPDATE res_company
        SET account_setup_coa_state = 'done'
        WHERE account_setup_coa_done = TRUE
        """
    )


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    cr = env.cr
    map_account_payment_term_line_option(cr)
    map_account_tax_type_tax_use(cr)
    fill_bank_statement_line_account_number(cr)
    fill_account_chart_template_account_code_prefix(cr)
    fill_account_payment_partner_bank_account_id(cr)
    fill_account_journal_alias_id(env)
#    fill_account_invoice_line_display_type(cr)
    update_res_company_account_setup_steps_states(cr)
    env['account.group']._parent_store_compute()
    openupgrade.load_data(
        cr, 'account', 'migrations/12.0.1.1/noupdate_changes.xml')
