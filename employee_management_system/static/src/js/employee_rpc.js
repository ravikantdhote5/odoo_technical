/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

export class MainComponent extends Component {
  static template = "employee_management_system.MainComponentTemplate";

  setup() {
    this.state = useState({recordCount: 0});
    this.loadData();
  }

  async loadData() {
    try {
      const result = await rpc('/employee_management_system/custom_rpc',{});

      this.state.recordCount = result.count;
      console.log("Record count:", this.state.recordCount);
    } catch (e) {
      console.error("RPC failed:", e);
    }
  }
}

console.log("Registering MainComponent...");
registry.category("actions").add("employee_management_system.MainComponent", MainComponent);
console.log("MainComponent registered successfully!");
