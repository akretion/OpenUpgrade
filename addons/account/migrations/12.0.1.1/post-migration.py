# Copyright 2018 Eficent <http://www.eficent.com>
# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tools.translate import _
from openupgradelib import openupgrade
from psycopg2.extensions import AsIs


def map_account_journal_bank_statements_source(cr):
    openupgrade.map_values(
        cr,
        openupgrade.get_legacy_name('bank_statements_source'),
        'bank_statements_source',
        [('manual', 'undefined'),
         ],
        table='account_journal', write='sql')


def map_account_payment_term_line_option(cr):
    openupgrade.logged_query(
        cr, """
        UPDATE account_payment_term_line
        SET days = 31
        WHERE option = 'last_day_following_month'
            OR option = 'last_day_current_month'
        """
    )
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
    openupgrade.logged_query(
        cr, """
        UPDATE account_tax
        SET type_tax_use = 'adjustment'
        WHERE type_tax_use = 'none' AND %s = TRUE
        """, (AsIs(openupgrade.get_legacy_name('tax_adjustment')), ),
    )
    openupgrade.logged_query(
        cr, """
        UPDATE account_tax_template
        SET type_tax_use = 'adjustment'
        WHERE type_tax_use = 'none' AND %s = TRUE
        """, (AsIs(openupgrade.get_legacy_name('tax_adjustment')), ),
    )


def fill_account_chart_template_account_code_prefix(cr):
    # if company_id was filled:
    openupgrade.logged_query(
        cr, """
        UPDATE account_chart_template act
        SET bank_account_code_prefix = rc.bank_account_code_prefix
        FROM res_company rc
        WHERE act.%s = rc.id AND act.bank_account_code_prefix IS NULL
        """, (AsIs(openupgrade.get_legacy_name('company_id')), ),
    )
    openupgrade.logged_query(
        cr, """
        UPDATE account_chart_template act
        SET cash_account_code_prefix = rc.cash_account_code_prefix
        FROM res_company rc
        WHERE act.%s = rc.id AND act.cash_account_code_prefix IS NULL
        """, (AsIs(openupgrade.get_legacy_name('company_id')), ),
    )
    # if company_id was not filled:
    openupgrade.logged_query(
        cr, """
        UPDATE account_chart_template act
        SET bank_account_code_prefix = 'OUB'
        WHERE act.bank_account_code_prefix IS NULL
        """
    )
    openupgrade.logged_query(
        cr, """
        UPDATE account_chart_template act
        SET cash_account_code_prefix = 'OUB'
        WHERE act.cash_account_code_prefix IS NULL
        """
    )
    # transfer_account_code_prefix:
    openupgrade.logged_query(
        cr, """
        UPDATE account_chart_template act
        SET transfer_account_code_prefix = trim(leading '0' from aat.code)
        FROM account_account_template aat
        WHERE act.%s = aat.id
        """, (AsIs(openupgrade.get_legacy_name('transfer_account_id')), ),
    )


def update_res_company_account_setup_steps_states(cr):
    openupgrade.logged_query(
        cr, """
        UPDATE res_company
        SET account_setup_bank_data_state = 'done'
        WHERE account_setup_bank_data_done = TRUE
        """
    )
    openupgrade.logged_query(
        cr, """
        UPDATE res_company
        SET account_setup_fy_data_state = 'done'
        WHERE account_setup_fy_data_done = TRUE
        """
    )
    openupgrade.logged_query(
        cr, """
        UPDATE res_company
        SET account_setup_coa_state = 'done'
        WHERE account_setup_coa_done = TRUE
        """
    )


def fill_account_journal_alias_id(env):
    journal_model = env["account.journal"]
    journals = journal_model.with_context(
        active_test=False).search([('type', '=', 'purchase')])
    for journal in journals:
        journal._update_mail_alias({})


def fill_account_move_reverse_entry_id(env):
    def fill_account_move_reverse_date(origin_move, reversal):
        reverser = env['res.users'].browse(reversal.create_uid)
        date = None
        if origin_move.reverse_date and (
                not reverser.company_id.period_lock_date
                or origin_move.reverse_date >
                reverser.company_id.period_lock_date):
            date = reversal.reverse_date
        reversal.reverse_date = date

    all_moves = env['account.move'].search([])
    if openupgrade.table_exists(env.cr, 'account_move_reverse'):
        reversal_moves = all_moves.filtered(lambda m: m.reverse_entry_id).\
            mapped('reverse_entry_id')
        for move in reversal_moves:
            origin = all_moves.filtered(
                lambda m: m.reverse_entry_id == move.id)
            fill_account_move_reverse_date(origin, move)
    else:
        reversal_moves = all_moves.filtered(
            lambda m: m.ref and m.ref.startswith(_('reversal of: ')))
        for move in reversal_moves:
            name = move.ref.partition(_('reversal of: '))[2]
            origin = all_moves.filtered(lambda m: m.name == name)[0]
            if not origin.reverse_entry_id:
                origin.reverse_entry_id = move.id
            fill_account_move_reverse_date(origin, move)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    map_account_journal_bank_statements_source(cr)
    map_account_payment_term_line_option(cr)
    map_account_tax_type_tax_use(cr)
    env['account.group']._parent_store_compute()
    fill_account_chart_template_account_code_prefix(cr)
    update_res_company_account_setup_steps_states(cr)
    fill_account_journal_alias_id(env)
    fill_account_move_reverse_entry_id(env)
    openupgrade.load_data(
        cr, 'account', 'migrations/12.0.1.1/noupdate_changes.xml')
