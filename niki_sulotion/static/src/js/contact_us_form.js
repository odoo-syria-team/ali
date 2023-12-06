doo.define('niki_sulotion.contact_us_attachment_form', function (require) {
    'use strict';
    var core = require('web.core');
    const dom = require('web.dom');
    var _t = core._t;

    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');
    var qweb = core.qweb;
    var rpc = require('web.rpc');

    publicWidget.registry.ContactUsAttachmentForm = publicWidget.Widget.extend({
        selector: '.s_website_form_send',

        events: {
        'click': '_onsubmit',
        },

        _onsubmit: function (ev) {
        ev.preventDefault();
        var files = document.getElementsByClassName('get_attach');
        var data_array = [];
        var count = 0;

        for (var i = 0; i < files.length; i++) {
            var selectedFile = new FileReader();
            selectedFile.addEventListener('load', function (e) {
                count++;
                const data = e.target.result;
                data_array.push(data);

                if (count === files.length) {
                    this._rpc({
                        route: '/web/attachment',
                        params: {
                            data: data_array,
                        },
                    });
                }
            }.bind(this));

            selectedFile.readAsDataURL(files[i].files[0]);
        }
    },

    })
});
