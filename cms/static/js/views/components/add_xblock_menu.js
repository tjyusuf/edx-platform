define(["jquery", "js/views/baseview", 'edx-ui-toolkit/js/utils/html-utils'],
    function ($, BaseView, HtmlUtils) {

        return BaseView.extend({
            className: function () {
                return "new-component-templates new-component-" + this.model.type;
            },
            initialize: function () {
                BaseView.prototype.initialize.call(this);
                var template_name = this.model.type === "problem" ? "add-xblock-component-menu-problem" :
                    "add-xblock-component-menu";
                var support_template = this.loadTemplate("add-xblock-component-support-level");
                this.template = this.loadTemplate(template_name);
                this.$el.html(this.template({
                    type: this.model.type, templates: this.model.templates,
                    allow_unsupported_xblocks: this.model.allow_unsupported_xblocks,
                    support_template: support_template, HtmlUtils: HtmlUtils
                }));
                // Make the tabs on problems into "real tabs"
                this.$('.tab-group').tabs();
            }
        });

    }); // end define();