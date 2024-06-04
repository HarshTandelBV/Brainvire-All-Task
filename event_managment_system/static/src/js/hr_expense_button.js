/* @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { listView } from "@web/views/list/list_view";
import { registry } from "@web/core/registry";
import { ExpenseListController } from '@hr_expense/views/list';

class HrExpenseListController extends ExpenseListController {
    setup(){
        super.setup()
        console.log('js is loaded')
    }
}

HrExpenseListController.template = 'event_managment_system.HrExpenseListViews'

export const hrExpenseListView = {
    ...listView,
    Controller: HrExpenseListController,
}

registry.category("views").add('hr_expense_list_view',hrExpenseListView)