# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields,osv
from openerp import tools
# from .. import crm



class forecastpro_report(osv.osv):
    """ Phone calls by user and section """

    _name = "forecastpro.weblot.report"
    _description = "Forecast PRO by PO, partner, product and other attributes"
    _auto = False

    _columns = {
        'ean13': fields.char('ISBN', readonly=True),
        'date_order': fields.date('Order Date', readonly=True, select=True),
        'year': fields.integer('Year', readonly=True),
        'month': fields.integer('Month', readonly=True),
        'product_id': fields.many2one('product.product', 'Product' , readonly=True),
        'sb_name': fields.char('SB Name', readonly=True, select=True),
	'boxes': fields.float('Boxes',readonly=True,select=True),
    }

    def init(self, cr):

        """ ForecastPro by PO, partner, date and product
        """
        tools.drop_view_if_exists(cr, 'forecastpro_weblot_report')
        cr.execute("""
            create or replace view forecastpro_weblot_report as (
		select b.id,pp.ean13 as ean13,
			a.date_order as date_order,
			date_part('year',a.date_order) as year,
			date_part('month',a.date_order) as month,
			b.product_id as product_id,
			rp_sb.name as sb_name,
			b.boxes as boxes 
			from purchase_order a inner join purchase_order_line b on a.id = b.order_id
			inner join product_product pp on pp.id = b.product_id 
			left join product_supplierinfo c on c.product_tmpl_id = pp.product_tmpl_id and c.name = a.partner_id 
			left join res_partner rp on rp.id = a.partner_id
			left join res_users ru on ru.id = a.create_uid left join res_partner rpc on rpc.id = ru.partner_id
			left join res_partner rp_sb on rpc.parent_id = rp_sb.id
			where a.state = 'approved'
            )""")

forecastpro_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
