/* @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.customWidget = publicWidget.Widget.extend({
    selector: '.oe_custom_button',

    events: {
        'click .btn-go-to-shop': '_onClickGoToShop',
    },

    start: function () {
        this._super.apply(this, arguments);
    },


    _onClickGoToShop: function () {
        window.location.href = '/shop';
    },
})
