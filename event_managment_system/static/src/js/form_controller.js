/* @odoo-module */

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { jsonrpc } from "@web/core/network/rpc_service";
import { formView } from "@web/views/form/form_view";
import { FormController } from "@web/views/form/form_controller";

export class SalesFormController extends FormController {
    setup() {
        super.setup();
        this.action = useService("action");
        this.ormService = useService("orm");
        console.log("This is sales form controller");
    };

    getData(){
        alert('hello')
    };


};
SalesFormController.template = "event_managment_system.FormViewBtn";

export const SaleModelFormView = {
    ...formView,
    Controller: SalesFormController,
}

registry.category("views").add("sale_form", SaleModelFormView);
