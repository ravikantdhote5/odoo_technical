/** @odoo-module **/

import { onWillStart, onWillRender,
         onMounted, onRendered,
         onWillUpdateProps, onWillPatch,
         onPatched, onWillUnmount,
          onWillDestroy, useEffect } from "@odoo/owl";
import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";


class CustomFormController extends FormController {
    setup() {
        super.setup();
        console.log("Custom Form Controller Initialized");

        useEffect(() => {
            console.log("Component mounted (useEffect)");
//        }, () => []);
        });

        onWillStart(async () => {
            console.log("onWillStart callback is running");
        });

        onWillRender(() => {
            console.log("onWillRender callback is running");
        });

        onMounted(() => {
            console.log("onMounted worked inside CustomFormController");
        });

        onRendered(() => {
            console.log("onRendered callback is running");
        });

        onWillPatch(() => {
            console.log("Component is ABOUT to update its DOM");
        });

        onPatched(() => {
            console.log("onPatched called — DOM has been updated!");
        });

        onWillUnmount(() => {
          console.log("Component is about to unmount");
        });

        onWillDestroy(() => {
            console.log("Component is Destroyed");
        });
    }
    }

export const customFormView = {
    ...formView,
    Controller: CustomFormController,
};

registry.category("views").add("custom_form", customFormView);
