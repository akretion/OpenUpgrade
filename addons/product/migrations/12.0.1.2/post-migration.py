# Copyright 2018 Eficent <http://www.eficent.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


def map_product_attribute_create_variant(cr):
    openupgrade.map_values(
        cr,
        openupgrade.get_legacy_name('create_variant'),
        'create_variant',
        [(False, 'no_variant'),
         (None, 'no_variant'),
         (True, 'always'),
         ],
        table='product_attribute', write='sql')


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    env['product.category']._parent_store_compute()
    map_product_attribute_create_variant(env.cr)
