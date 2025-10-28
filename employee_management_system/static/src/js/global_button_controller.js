/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { ListController } from '@web/views/list/list_controller';
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { useService } from "@web/core/utils/hooks";

patch(ListController.prototype, {
    setup() {
        super.setup();
        this.dialogService = useService("dialog");
    },

    handleClick() {
        const model = this.actionService.currentController.action.res_model;
        const module = this.actionService.currentController.action.xml_id;

        const val = module
            ? module
                .split('.')[0]
                .split('_')
                .map(w => w.charAt(0).toUpperCase() + w.slice(1))
                .join(' ')
            : 'Unknown Module';

        this.dialogService.add(ConfirmationDialog, {
            body: `Model: ${model}\nModule: ${val}`,
            confirm: () => { },
            cancel: () => { },
        });
    },
});
