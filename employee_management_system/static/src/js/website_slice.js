/** @odoo-module **/

import publicWidget from '@web/legacy/js/public/public_widget';

console.log('ProductQuantityOutput JS loaded!');

publicWidget.registry.ProductQuantityOutput = publicWidget.Widget.extend({
    selector: '.o_website_qty_output_component',

    events: {
        'change input[name="add_qty"]': '_onQtyChange',
        'input  input[name="add_qty"]': '_onQtyChange',
    },

    start() {
        const result = this._super.apply(this, arguments);

        $(document).on('input change', 'input[name="add_qty"]', this._onQtyChange.bind(this));
        $('input[name="add_qty"]').trigger('input');

        return result;
    },

    _onQtyChange(ev) {
        const $input = $(ev.currentTarget);
        const qty = parseFloat($input.val()) || 0;
        const factor = parseFloat(this.$el.data('conversion-factor')) || 1;
        const total = qty * factor;

        this.$el.find('input[name="slices_per_pizza"]').val(total);

    },
});


export default publicWidget.registry.ProductQuantityOutput;