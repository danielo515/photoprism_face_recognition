// Snowpack Configuration File
// See all supported options: https://www.snowpack.dev/#configuration

/** @type {import("snowpack").SnowpackUserConfig } */
module.exports = {
    mount: {
        src: '/',
    },
    exclude: ['./src/styles/*'],
    plugins: [['@snowpack/plugin-run-script', { cmd: 'yarn css --watch' }]],
    // installOptions: {},
    install: ['hyperhtml'],
    devOptions: {
        port: 4000,
    },
    buildOptions: {
        out: '../server/static',
        clean: true,
    },
    proxy: {
        '/app': 'http://localhost:5000',
    },
};
