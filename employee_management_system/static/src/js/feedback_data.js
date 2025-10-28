/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class EmployeeFeedbackList extends Component {
    static template = "employee_management_system.EmployeeFeedbackListTemplate";

    setup() {
        this.orm = useService("orm");
        this.state = useState({ feedbacks: [] });
        this.loadFeedbacks();
    }

    async loadFeedbacks() {
    try {
        const feedbackIds = await this.orm.call("employee.feedback", "search", [[]]);
        const records = await this.orm.call("employee.feedback", "read", [feedbackIds, ["name", "email", "comments"]]);
        this.state.feedbacks = records;
    } catch (e) {
        console.error("Failed to load feedbacks:", e);
    }
}
}

registry.category("actions").add("employee_management_system.EmployeeFeedbackList", EmployeeFeedbackList);
