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



class volumetrics_report(osv.osv):
    """ Phone calls by user and section """

    _name = "volumetrics.weblot.report"
    _description = "Volumetrics by PO, partner, product and other attributes"
    _auto = False

    STATE_SELECTION = [
        ('draft', 'Draft PO'),
        ('sent', 'RFQ'),
        ('bid', 'Bid Received'),
        ('confirmed', 'Waiting Approval'),
        ('approved', 'Purchase Confirmed'),
        ('except_picking', 'Shipping Exception'),
        ('except_invoice', 'Invoice Exception'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ]

    
    _columns = {
        'ean13': fields.char('ISBN', readonly=True),
        'publishing_bs': fields.many2one('product.publishing_bs', 'Publishing BS' , readonly=True),
        'paper_colour': fields.many2one('product.paper_colour', 'Paper Colour' , readonly=True),
        # 'publishing_bs': fields.char('Publishing BS', readonly=True),
        'default_code': fields.char('UBS Code', readonly=True),
        'po_name': fields.char('PO Name', readonly=True),
        'partner_id': fields.many2one('res.partner', 'Supplier' , readonly=True),
        'partner_ref': fields.char('Supplier', readonly=True),
        'date_order': fields.date('Order Date', readonly=True, select=True),
        'product_id': fields.many2one('product.product', 'Product' , readonly=True),
        'state': fields.selection(STATE_SELECTION, 'Status', readonly=True, help="The status of the purchase order or the quotation request. A request for quotation is a purchase order in a 'Draft' status. Then the order has to be confirmed by the user, the status switch to 'Confirmed'. Then the supplier must confirm the order to change the status to 'Approved'. When the purchase order is paid and received, the status becomes 'Done'. If a cancel action occurs in the invoice or in the reception of goods, the status becomes in exception.", select=True),
        'sb_name': fields.char('SB Name', readonly=True, select=True),
	'lote_id': fields.many2one('elote.lote','Lote',readonly=True,select=True),
        'qty': fields.float('Qty', readonly=True, select=True),
        'price_unit': fields.float('Price Unit', readonly=True, select=True),
        'amount': fields.float('Amount', readonly=True, select=True),
        'carton_quantity': fields.float('Carton Quantity', readonly=True, select=True),
        'carton_volume': fields.float('Carton Volume', readonly=True, select=True),
        'weight': fields.float('Weight', readonly=True, select=True),
        'porc_teu': fields.float('% TEU', readonly=True, select=True),
        'additional_cost': fields.float('Additional Cost', readonly=True, select=True),
	'boxes': fields.float('Boxes',readonly=True,select=True),
	'total_amount': fields.float('Total Amount',readonly=True,select=True)
    }

    def init(self, cr, uid=1):

        """ Volumetrics by PO, partner, date and product
        """
        tools.drop_view_if_exists(cr, 'volumetrics_weblot_report')
        cr.execute("""
            create or replace view volumetrics_weblot_report as (
		select b.id,pp.ean13 as ean13,pp.publishing_bs as publishing_bs,pp.paper_colour,pp.default_code as default_code,
			a.name as po_name,
			a.partner_id as partner_id ,
			rp.ref as partner_ref,
			a.date_order as date_order,b.product_id as product_id,a.state,rp_sb.name as sb_name,a.lote_id as lote_id,
			b.product_qty as qty,b.price_unit as price_unit,b.product_qty * b.price_unit as amount,
			case when (c.carton_quantity is null or c.carton_quantity = 0) then 0 else c.carton_quantity end as carton_quantity,
			case when (c.carton_quantity is null or c.carton_quantity = 0) then 0 else ceil(b.product_qty / c.carton_quantity) * c.carton_volume end as carton_volume,
			case when (c.carton_quantity is null or c.carton_quantity = 0) then 0 else b.boxes * c.carton_weight end as weight,
			b.boxes * c.carton_volume as porc_teu,
			b.product_qty  * ((c.service_fee/100*c.supplier_price)+c.royalties+c.developing_cost) as additional_cost,
			b.boxes as boxes,
			b.product_qty  * ((c.service_fee/100*c.supplier_price)+c.royalties+c.developing_cost) + b.product_qty * b.price_unit as total_amount 
			from purchase_order a inner join purchase_order_line b on a.id = b.order_id
			inner join product_product pp on pp.id = b.product_id 
			left join product_supplierinfo c on c.product_tmpl_id = pp.product_tmpl_id and c.name = a.partner_id 
			left join res_partner rp on rp.id = a.partner_id
			left join res_users ru on ru.id = a.create_uid left join res_partner rpc on rpc.id = ru.partner_id
			left join res_partner rp_sb on rpc.parent_id = rp_sb.id)""")

volumetrics_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
