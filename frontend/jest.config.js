module.exports = {
    preset: "@vue/cli-plugin-unit-jest",
    transform: {
        "^.+\\.vue$": "vue-jest",
    },
    reporters: ["default", "jest-junit"],
    verbose: true,
    collectCoverage: true,
    collectCoverageFrom: [
        "**/*.{js,jsx,vue}",
        "!**/node_modules/**",
        "!**/vendor/**",
    ],
    coverageReporters: ["lcov"],
    coverageDirectory: "./coverage",
};
