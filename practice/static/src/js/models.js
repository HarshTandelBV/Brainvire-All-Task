/** @odoo-module **/

import { Order,Orderline } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.custom_note = this.custom_note || "";
        this.discount_applied = false;
        this.location = this.location || "";
    },

    //@override
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        if (json) {
            json.discount_applied = this.discount_applied;
            json.custom_note = this.custom_note;
            json.location = this.location.name;
        }
        return json;
    },

    //@override
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.discount_applied = json.discount_applied || false;
        this.custom_note = json.custom_note;
        this.location = json.location;
    },

    //@override
    export_for_printing() {
        const result = super.export_for_printing(...arguments);
        result.custom_note = this.custom_note;
        result.location = this.location.name;
        return result;
    },

    getCustomNote() {
        return this.custom_note;
    },


    setCustomNote(note) {
        this.custom_note = note || "";
    },

    getDiscountApplied() {
        this.disount_applied;
    },

    setDiscountApplied() {
        this.disount_applied = true;
    },

});

