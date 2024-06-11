/* @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";
import PortalSidebar from "@portal/js/portal_sidebar";

PortalSidebar.include({
    selector: ".o_portal_purchase_sidebar",

    init: function (parent, options) {
        this._super.apply(this, arguments);
        console.log("Custom functionality: PurchasePortalSidebar initialized");
    },

    start: function () {
        this.$el.css('background-color', '#d7d2d7');
        this.$el.css('border-radius', '15px');

        let element = document.querySelector(".col-lg-3.col-xl-4.d-print-none");
        if (element) {
            element.style.backgroundColor = '#cdd0dc';
            element.style.borderTopLeftRadius = '15px';
            element.style.borderBottomLeftRadius = '15px';
            element.addEventListener('click', function(){
                alert("It's a Sidebar of Purchase Orders")
            })
        } else {
            console.warn("Element with class 'col-lg-3 col-xl-4 d-print-none' not found");
        }

        let customer_support = document.getElementById('contact_us');
        if(customer_support) {
            customer_support.addEventListener('click',function(e){
                alert("Customer Support Clicked");
                e.stopPropagation();
            })
        }

        this.$el.on('click', '#contact_us', function() {
            window.location.href = '/contactus';
        });
    },
});
