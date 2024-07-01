/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Component, onWillStart, useState } from "@odoo/owl";

export class OrderListScreen extends Component {
    setup() {
        this.state = useState({ orders: [] });
        this.orm = useService("orm");
        this.pos = usePos();
        onWillStart(async () => {
            await this.loadOrders();
        });
    }

    async loadOrders() {
        try {
            const orders = await this.orm.call(
                "pos.order",
                "search_read",
                [[['config_id', '=', this.pos.config.id]], ['name', 'pos_reference', 'date_order', 'partner_id', 'employee_id', 'amount_total', 'state']]
            );
            console.log(orders);
            this.state.orders = orders;
        } catch (error) {
            console.error('Error fetching orders:', error);
        }
    }

    onCreateNewOrder() {
        this.pos.add_new_order();
        this.pos.showScreen("ProductScreen");
    }

}

OrderListScreen.template = 'point_of_sale.OrderListScreen';
registry.category("pos_screens").add("OrderListScreen", OrderListScreen);
