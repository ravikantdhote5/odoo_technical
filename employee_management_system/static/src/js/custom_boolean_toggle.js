/** @odoo-module **/
import { BooleanField } from "@web/views/fields/boolean/boolean_field";
import { registry } from "@web/core/registry";

export class CustomBooleanToggle extends BooleanField {
    async onChange(value) {
        this.state.value = value;
        await this.props.record.update({ [this.props.name]: value });
        setTimeout(() => {
            var sheet = document.querySelector(".o_form_sheet");
            if (sheet) sheet.style.backgroundColor = value ? "#d1ffd1" : "#ffffff";
        }, 50);
    }

//    mounted() {
//        setTimeout(() => {
//            var sheet = document.querySelector(".o_form_sheet");
//            if (sheet) sheet.style.backgroundColor = this.props.value ? "#d1ffd1" : "#ffffff";
//        }, 50);
//    }
}


registry.category("fields").add("custom_boolean_toggle", {
    component: CustomBooleanToggle
});
