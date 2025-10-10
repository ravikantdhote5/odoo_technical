/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

class GlButton extends Component {

  handleClick() {
    const resModel = this.props?.res_model || "";
    const moduleName = resModel.split(".")[0] || "";
    alert("Module: " + moduleName);
  }
}

registry.category("actions").add("employee_management_system.GlButton", GlButton);
