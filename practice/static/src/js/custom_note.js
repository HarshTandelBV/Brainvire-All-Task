/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { TextAreaPopup } from "@point_of_sale/app/utils/input_popups/textarea_popup";

class AddNotes extends Component {
    static template = "point_of_sale.AddNotesButton";

    setup() {
        this.popup = useService("popup");
        this.pos = useService("pos");
    }

    async onAddItemNote() {
        const currentOrder = this.pos.get_order();
        if (!currentOrder) {
            this.popup.add(ErrorPopup, {
                title: _t("No Order Found"),
                body: _t("Please create an order first!"),
            });
            return;
        }

        const { confirmed, payload: inputNote } = await this.popup.add(TextAreaPopup, {
            startingValue: currentOrder.getCustomNote(),
            title: _t("Add Customer Note Here"),
        });

        if (confirmed) {
            currentOrder.setCustomNote(inputNote);
        }
    }
};

ProductScreen.addControlButton({
    component: AddNotes,
    position: ["after", "SetSaleOrderButton"],
});
