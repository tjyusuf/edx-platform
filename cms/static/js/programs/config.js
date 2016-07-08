require.config({
    baseUrl: '/static/',
    paths: {
        'backbone': 'bower_components/backbone/backbone',
        // We're intentionally using code from this package's src/ directory, which includes
        // a bug fix that hasn't yet made it over to the code in dist/.
        // See: https://github.com/thedersen/backbone.validation/commit/1b949.
        'backbone.validation': 'bower_components/backbone.validation/src/backbone-validation',
        'gettext': 'js/programs/shims/gettext',
        'jquery': 'bower_components/jquery/dist/jquery',
        'jquery-cookie': 'bower_components/jquery-cookie/jquery.cookie',
        'requirejs': 'bower_components/requirejs/require',
        'text': 'bower_components/text/text',
        'underscore': 'bower_components/underscore/underscore'
    },
    shim: {
        'backbone.validation': {
            deps: ['backbone', 'underscore']
        },
        'jquery.cookie': {
            deps: ['jquery']
        }
    }
});
