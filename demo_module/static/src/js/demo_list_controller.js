/* @odoo-module */

import { registry } from "@web/core/registry";
import { listView } from '@web/views/list/list_view';
import { ListController } from '@web/views/list/list_controller';
import { useService } from "@web/core/utils/hooks";
import { jsonrpc } from "@web/core/network/rpc_service";

export class DemoListController extends ListController {
    setup() {
        super.setup();
        this.action = useService("action");
        this.ormService = useService("orm");
        this.notification = useService("notification"); // Added initialization for notification service
        console.log("This is demo controller");
    }

    getOrderSatusData() {
        console.log('Data Button');
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Order Status',
            res_model: 'demo.order.status',
            views: [[false, "list"], [false, "form"]]
        });
    }

    async getData() {
        console.log('Excel Data');
        const selectedRecords = this.model.root.selection.map((datapoint) => datapoint.resId);
        console.log('Selected Record IDs:', selectedRecords);

        if (!selectedRecords.length) {
            this.notification.add('Please select at least one record.', {
                title: 'No records selected',
                type: 'warning',
            });
            return;
        }

        try {
            const response = await jsonrpc('/web/dataset/call_kw/demo.customer.report/print_xlsx_report', {
                model: 'demo.customer.report',
                method: 'print_xlsx_report',
                args: [selectedRecords],
                kwargs: {}
            });

            console.log('RPC Response:', response);

            if (response && response.url) {
                // Trigger download
                window.location.href = response.url;
                this.notification.add('Excel Report Downloaded successfully!', {
                    title: 'Success',
                    type: 'success',
                });
            } else {
                this.notification.add('Failed to get the download URL.', {
                    title: 'Error',
                    type: 'danger',
                });
            }
        } catch (error) {
            console.error('Error during RPC call:', error);
            this.notification.add('Failed to download excel Report.', {
                title: 'Error',
                type: 'danger',
            });
        } finally {
            console.log('It will work always');
        }
    }
}

registry.category('views').add('demo_list', {
    ...listView,
    Controller: DemoListController,
    buttonTemplate: "demo_module.ListView.Buttons",
});
