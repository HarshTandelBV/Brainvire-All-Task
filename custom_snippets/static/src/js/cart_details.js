/** @odoo-module **/

import { jsonrpc } from "@web/core/network/rpc_service";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.CartDetailsSnippet = publicWidget.Widget.extend({
    selector: '.cart-details',
    start: function () {
        this._super.apply(this, arguments);
        this._updateCartDetails();
    },
    _updateCartDetails: async function () {
        try {
            const result = await jsonrpc("/shop/cart/get_cart_details", {});
            if (result) {
                document.getElementById('total-items').innerText = result.total_items;
                document.getElementById('total-amount').innerText = `$${result.total_amount}`;
            }
        } catch (error) {
            console.error("Failed to fetch cart details:", error);
        }
    },
});
