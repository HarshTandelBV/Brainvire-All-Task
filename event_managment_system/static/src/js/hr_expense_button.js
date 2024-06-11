/* @odoo-module */
import { ExpenseListController } from '@hr_expense/views/list';
import { patch } from "@web/core/utils/patch";
import { jsonrpc } from "@web/core/network/rpc_service";

patch(ExpenseListController.prototype, {
    async sendEmail() {
    console.log(this)
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
        await jsonrpc('/web/dataset/call_kw/hr.expense/action_send_email', {
            model: 'hr.expense',
            method: 'action_send_email',
            args: [selectedRecords],
            kwargs: {}
        });
        this.notification.add('Emails sent successfully!', {
            title: 'Success',
            type: 'success',
        });
    } catch (error) {
        console.error('Error during RPC call:', error);
        this.notification.add('Failed to send emails.', {
            title: 'Error',
            type: 'danger',
        });
    } finally {
        console.log('It will works always');
    }
}

});
