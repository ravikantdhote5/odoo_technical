/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import ControlPanel from "web.ControlPanel";
import { useState } from "@odoo/owl";

patch(ControlPanel.prototype, "employee_management_system.ControlPanelPatch", {
    setup() {
        this._super();
        this.state = useState({ moduleName: null });
    },
    showModuleName() {
        const action = this.env.action || {};
        if (action.res_model) {
            this.state.moduleName = action.res_model.split(".")[0].charAt(0).toUpperCase() + action.res_model.split(".")[0].slice(1);
        } else {
            this.state.moduleName = "Unknown Module";
        }
    }
});
