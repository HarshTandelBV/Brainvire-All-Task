/** @odoo-module **/

import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Component, useState } from "@odoo/owl";
import { PosDB } from "@point_of_sale/app/store/db";
import { useService } from "@web/core/utils/hooks";

export class SetLocationButton extends Component {
    static template = "point_of_sale.SetLocationButton";
    setup() {
        this.pos = usePos();
        this.orm = useService("orm");
        this.db = new PosDB();

        this.state = useState({
            selectedLocationName: "",
        });

        this.updateSelectedLocationLabel();
    }

    async updateSelectedLocationLabel() {
        try {
            const currentOrder = this.pos.get_order();
            if (currentOrder.location) {
                this.state.selectedLocationName = currentOrder.location.name;
            } else {
                this.state.selectedLocationName = "Location"; // Default label when no location is selected
            }
        } catch (error) {
            console.error("Error updating location label:", error);
        }
    }

    async click() {
        const config_id = this.pos.config.id;
//        console.log(config_id);
        const current_order = this.pos.get_order();
        if(!current_order.get_partner()){
            return
        }
        this.pos.showScreen("LocationListScreen");
    }
}

ProductScreen.addControlButton({ component: SetLocationButton });