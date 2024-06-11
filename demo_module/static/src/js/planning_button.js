/* @odoo-module */
import { GanttController } from "@web_gantt/gantt_controller";
import { patch } from "@web/core/utils/patch";
import { PlanningGanttController } from "@planning/views/planning_gantt/planning_gantt_controller";

patch(PlanningGanttController.prototype,{
    async popup() {
        alert('Pop up')
    }
});