// module.exports = {
//   root: true,
//   env: {
//     node: true
//   },
//   'extends': [
//     'plugin:vue/vue3-essential',
//     'eslint:recommended'
//   ],
//   parserOptions: {
//     parser: 'babel-eslint'
//   },
//   rules: {
//     'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
//     'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off'
//   }
// };

module.exports = {
    root: true,
    "env": {
        "browser": true,
        "commonjs": true,
        "es6": true,
        "node": true
    },

    "parser": "vue-eslint-parser",

    "parserOptions": {
        parser: 'babel-eslint',
        "ecmaFeatures": {
            // "jsx": true
        },
        "allowImportExportEverywhere": true,
        "sourceType": "module"
    },

    // https://github.com/feross/standard/blob/master/RULES.md#javascript-standard-style
    //   "extends": "standard",
    // required to lint *.vue files
    //   "plugins": [
    //       "html"
    //   ]
    "rules": {
        "no-multiple-empty-lines": [2, { "max": 2, "maxEOF": 1 }],
        "no-mixed-operators": 0,
        "no-debugger": 0,
        "no-const-assign": "warn",
        "no-this-before-super": "warn",
        "no-undef": "warn",
        "no-unreachable": "warn",
        "no-unused-vars": "warn",
        "no-console": "off",
        "constructor-super": "warn",
        "valid-typeof": "warn"
    },
    plugins: ['vue'],
    overrides: [
      {
        files: [
          '**/__tests__/*.{j,t}s?(x)',
          '**/tests/unit/**/*.spec.{j,t}s?(x)'
        ],
        env: {
          jest: true,
          // jQuery: true
        }
      }
    ]
}
// http://eslint.org/docs/user-guide/configuring
