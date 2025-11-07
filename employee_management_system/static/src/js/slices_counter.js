/** @odoo-module **/

import publicWidget from '@web/legacy/js/public/public_widget';

console.log('PizzaSlicesCounter JS loaded!');
publicWidget.registry.PizzaSlicesCounter = publicWidget.Widget.extend({
    selector: '.o_wsale_slices_counter',
    events: {
        'change input[name="add_qty"]': '_onQtyChange',
        'input  input[name="add_qty"]': '_onQtyChange',
    },

    _onQtyChange(ev) {
        console.log('Quantity changed!', ev);
        const $input  = $(ev.currentTarget);
        const qty = $input.val() || 1;
        const slicesPer = parseInt(this.$('.slices-input').val()) || 0;
        const totalSlices = qty * slicesPer;
        console.log('Qty:', qty, 'Slices per pizza:', slicesPer, 'Total:', totalSlices);
        this.$el.find('.slices_count_display').text(totalSlices);
    },

    start() {
    const result = this._super.apply(this, arguments);
    $(document).on('input change', 'input[name="add_qty"]', this._onQtyChange.bind(this));
    $('input[name="add_qty"]').trigger('input');
    return result;
    },
    });

export default publicWidget.registry.PizzaSlicesCounter;
