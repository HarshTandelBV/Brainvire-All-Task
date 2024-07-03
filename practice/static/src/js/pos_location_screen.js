/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Component, onWillStart, useState } from "@odoo/owl";

export class LocationListScreen extends Component {
    setup() {
        this.state = useState({ locations: [] });
        this.orm = useService("orm");
        this.pos = usePos();

        onWillStart(async () => {
            await this.loadLocations();
        });
    }

    async loadLocations() {
        try {
            const locations = await this.orm.call(
                "res.location",
                "search_read",
                [[['id', 'in', this.pos.config.location_ids]], ['id', 'name']]
            );
            this.state.locations = locations;
        } catch (error) {
            console.error('Error fetching locations:', error);
        }
    }

    async selectLocation(locationId) {
        try {
            // Update the current order with the selected location
            const selectedLocation = this.state.locations.find(loc => loc.id === locationId);
            if (selectedLocation) {
                const currentOrder = this.pos.get_order();
                currentOrder.location = selectedLocation;
                console.log(currentOrder)
            }
        } catch (error) {
            console.error('Error selecting location:', error);
        } finally {
            // Close the location selection screen and navigate back to ProductScreen
            this.pos.showScreen("ProductScreen");
        }
    }
}

LocationListScreen.template = 'point_of_sale.LocationListScreen';
registry.category("pos_screens").add("LocationListScreen", LocationListScreen);
