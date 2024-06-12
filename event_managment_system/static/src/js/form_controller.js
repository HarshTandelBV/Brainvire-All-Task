/* @odoo-module */

import { registry } from "@web/core/registry";
import { formView } from '@web/views/form/form_view';
import { useService } from "@web/core/utils/hooks";
import { jsonrpc } from "@web/core/network/rpc_service";
import { AccountMoveController } from "@account/components/account_move_form/account_move_form";

export class EventManagmentFormController extends AccountMoveController {
    setup() {
        super.setup();
        this.action = useService("action");
        this.ormService = useService("orm");
        console.log("This is demo controller");
    }


}

registry.category('views').add('event_list', {
    ...formView,
    Controller: EventManagmentFormController,
    buttonTemplate: "event.FormView.Buttons",
});
