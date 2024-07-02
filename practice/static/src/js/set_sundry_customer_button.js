/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { PartnerListScreen } from "@point_of_sale/app/screens/partner_list/partner_list";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { _t } from "@web/core/l10n/translation";

patch(PartnerListScreen.prototype, {
    setup() {
        super.setup(...arguments);
        this.orm = useService("orm");
        this.popup = useService("popup");
        this.pos = usePos();
    },
    async setSundryCustomer() {
         const sundryCustomer = await this.orm.searchRead('res.partner', [['name', '=', 'Sundry Customer']], ['id']);

        if (sundryCustomer.length > 0) {
            const sundryCustomerId = sundryCustomer[0].id;
            const partner = this.pos.db.get_partner_by_id(sundryCustomerId);
            console.log('Sundry Customer ID:', sundryCustomerId);
            this.state.selectedPartner = partner;
            this.confirm();

        } else {
            this.popup.add(ErrorPopup, {
                    title: _t("Error"),
                    body: _t(
                        "Customer Not Found",
                    ),
                });
            this.confirm();
            console.log('Sundry Customer not found');

        }
    }
});
