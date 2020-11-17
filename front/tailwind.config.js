module.exports = {
    future: {
        // removeDeprecatedGapUtilities: true,
        purgeLayersByDefault: true,
    },
    purge: {
        layers: ['utilities'],
        content: ['../server/templates/*.html.jinja', './src/*.js'],
    },
    theme: {
        extend: {},
    },
    variants: {},
    plugins: [],
};
