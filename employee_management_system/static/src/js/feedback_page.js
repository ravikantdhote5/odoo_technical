/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class FeedbackPage extends Component {
    static template = "employee_management_system.FeedbackTemplate";

    setup() {
        this.orm = useService("orm");
        this.feedback = useState({
          name: '',
          email: '',
          comments: '',
        });
    }

    async submitFeedback(ev) {
        ev.preventDefault();
        try {
                await this.orm.call("employee.feedback", "create", [this.feedback]);

            alert("Feedback sent!");
            this.feedback.name = '';
            this.feedback.email = '';
            this.feedback.comments = '';
        } catch (e) {
            console.error(e);
            alert("Failed to send feedback.");
        }
    }
}

registry.category("actions").add("employee_management_system.FeedbackPage", FeedbackPage);
