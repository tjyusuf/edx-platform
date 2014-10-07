define([
    'domReady!', 'jquery', 'js/models/settings/course_details', 'js/views/settings/main'
], function(doc, $, CourseDetailsModel, MainView) {
    'use strict';
    return function (detailsUrl) {
        var model;
        // highlighting labels when fields are focused in
        $('form :input')
            .focus(function() {
                $('label[for="' + this.id + '"]').addClass('is-focused');
            })
            .blur(function() {
                $('label').removeClass('is-focused');
            });

        model = new CourseDetailsModel();
        model.urlRoot = detailsUrl;
        model.fetch({
            success: function(model) {
                var editor = new MainView({
                    el: $('.settings-details'),
                    model: model
                });
                editor.render();
            },
            reset: true
        });
    };
});
