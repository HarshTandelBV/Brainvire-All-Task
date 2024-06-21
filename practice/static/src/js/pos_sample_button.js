/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { ConfirmPopup } from "@point_of_sale/app/utils/confirm_popup/confirm_popup";
import { OfflineErrorPopup } from "@point_of_sale/app/errors/popups/offline_error_popup";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
import { ClosePosPopup } from "@point_of_sale/app/navbar/closing_popup/closing_popup";

class PosSampleButton extends Component {
    static template = "point_of_sale.PosSampleButton";

    setup() {
        this.popup = useService("popup");
        this.pos = useService("pos");
        console.log('hello world');
    }
    async onClick(){
//         this.popup.add(ErrorPopup, {
//            title: _t("Error Popup"),
//            body: _t("Simple error message."),
//        });

//        this.popup.add(ConfirmPopup, {
//            title: _t("Confirm Popup"),
//            body: _t("Are you sure you want to continue?"),
//            confirmText:'Yes',
//            cancelText: 'No'
//        });

//         this.popup.add(OfflineErrorPopup, {
//            title: _t("Offline Error Popup"),
//            body: _t("Don't take it seriously!")
//        });

//        this.popup.add(SelectionPopup, {
//            title: _t("You need Digital Card?"),
//            list: [{'id':0,'label':'Yes','item':false},
//                {'id':1,'label':'No','item':false},
//                {'id':2,'label':'Not Sure','item':false}]
//        });

//        const info = await this.pos.getClosePosInfo();
//        this.popup.add(ClosePosPopup, {
//            ...info,
//            keepBehind: true
//        });

        const selectedLine = this.pos.get_order().get_selected_orderline()
        this.pos.get_order().removeOrderline(selectedLine)
//        console.log(this.pos.get_order())
//        console.log(this.pos.get_order().get_orderlines())
//        console.log(selectedLine)

        console.log('Button Triggered');
    };

    async removeAllRecord(){
        const selectedLines = this.pos.get_order().get_orderlines()
        for (var i of selectedLines){
         this.pos.get_order().removeOrderline(i)
        }
    };
};

ProductScreen.addControlButton({
    component: PosSampleButton,
    position: ["before", "OrderlineCustomerNoteButton"]
});
