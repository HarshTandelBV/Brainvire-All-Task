/* @odoo-module */

import { registry } from "@web/core/registry";
import publicWidget from '@web/legacy/js/public/public_widget';
import { jsonrpc } from "@web/core/network/rpc_service";

publicWidget.registry.SearchSaleModal = publicWidget.Widget.extend({
    selector: '#search_popup',
    events: {
        'submit #search_order': '_onSubmitSearchForm',
    },
    _onSubmitSearchForm: function (event) {
        console.log("jay shree ram");
        event.preventDefault();
        var self = this;
        var searchQuery = this.$('#searchInput').val();
        console.log(searchQuery)

        jsonrpc('/sale_order_search', {search_query: searchQuery}).then(function (result) {
            var resultsHtml = '';
            console.log('resultsHtml')
            if (result.length > 0) {
                console.log('resultsHtml')
                result.forEach(function (order) {
                    console.log(order)
                    let link = order.portal_url;  // Use the URL from the response
                    resultsHtml += `
                        <table class="table">
                            <tr><th>Sale Order Number</th><td><a href="${link}">${order.name}</a></td></tr>
                            <tr><th>Products</th><td>${order.products}</td></tr>
                            <tr><th>Total Amount</th><td>${order.amount_total}</td></tr>
                            <tr><th>Tax</th><td>${order.tax}</td></tr>
                        </table>
                    `;
                });
            } else {
                resultsHtml = '<p>No matching sale orders found.</p>';
            }
            self.$('#order_details').html(resultsHtml);
        }).catch(function (error) {
            console.error('RPC Query Error:', error);
        });
    },
});

registry.category("widgets").add("SearchModal", publicWidget.registry.SearchModal);