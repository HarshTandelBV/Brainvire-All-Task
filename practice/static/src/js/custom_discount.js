/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { NumberPopup } from "@point_of_sale/app/utils/input_popups/number_popup";
import { jsonrpc } from "@web/core/network/rpc_service";

class OverallDiscount extends Component {
    static template = "point_of_sale.OverallDiscount";

    setup() {
        this.orm = useService("orm");
        this.popup = useService("popup");
        this.pos = useService("pos");
        console.log('hello world');
    }

    async onOverallDiscount() {
        const selectedLines = this.pos.get_order().get_orderlines();
        if (!selectedLines || selectedLines.length === 0) {
            this.popup.add(ErrorPopup, {
                title: _t("OrderLine is not selected"),
                body: _t("Please select an order first!"),
            });
            return;
        }
        const result = await this.orm.call("ir.config_parameter", "get_param", [
            "practice.custom_discount",
        ]);

        const custom_discount = parseFloat(result);

        if (custom_discount >= 100 || custom_discount <= 0 || isNaN(custom_discount)) {
            this.popup.add(ErrorPopup, {
                title: _t("Invalid discount value"),
                body: _t("Please enter a valid discount value between 1 and 99!"),
            });
            return;
        }

        for (let selectedLine of selectedLines) {
            selectedLine.set_discount(custom_discount);
        }
        const currentOrder = this.pos.get_order();
        console.log(this.pos.get_order());
        currentOrder.discount_applied = true;
    }
}

ProductScreen.addControlButton({
    component: OverallDiscount,
    position: ["after", "SetSaleOrderButton"],
});
