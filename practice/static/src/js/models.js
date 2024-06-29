/** @odoo-module **/

import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.custom_note = this.custom_note || "";
    },

    //@override
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        if (json) {
            json.custom_note = this.custom_note;
        }
        return json;
    },

    //@override
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.custom_note = json.custom_note;
    },

    getCustomNote() {
        return this.custom_note;
    },

    setCustomNote(note) {
        this.custom_note = note || "";
    },
});
