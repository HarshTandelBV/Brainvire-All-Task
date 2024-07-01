/** @odoo-module **/

import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Component } from "@odoo/owl";
import { PosDB } from "@point_of_sale/app/store/db";
import { useService } from "@web/core/utils/hooks";

export class SetOrderButton extends Component {
    static template = "point_of_sale.SetOrderButton";
    setup() {
        this.pos = usePos();
        this.orm = useService("orm");
        this.db = new PosDB();
    }
    async click() {
        const config_id = this.pos.config.id;
//        const order = this.pos.get_order();
//        const partner = order.get_partner();


        console.log(config_id)
        console.log(this.db.get_orders())
        this.pos.showScreen("OrderListScreen");
    }
}

ProductScreen.addControlButton({ component: SetOrderButton });