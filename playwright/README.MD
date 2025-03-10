
# Playwright Installation and Getting Started

This document outlines the steps for installing Playwright and getting started with writing end-to-end tests.

## Installation
1. install nodejs which comes with npm
2. add nodejs to system path
3. install playwright vscode extension
4. Set-ExecutionPolicy RemoteSigned
5. install playwright browsers: npm init playwright@latest --yes "--" . '--quiet' '--browser=chromium' '--browser=webkit' '--gha'

tests and tests-excamples folders are the key folders

6. npm install -g playwright

> npx
> create-playwright . --quiet --browser=chromium --browser=webkit --gha

Getting started with writing end-to-end tests with Playwright:
Initializing project in '.'
Initializing NPM project (npm init -y)…
Wrote to F:\github\helloworld\package.json:

{
  "name": "helloworld",
  "version": "1.0.0",
  "description": "a test! hello world from Kai, files for self-reference\r and have some more tests",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "repository": {
    "type": "git",
    "url": "git+https://github.com/cmskzhan/helloworld.git"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "bugs": {
    "url": "https://github.com/cmskzhan/helloworld/issues"
  },
  "homepage": "https://github.com/cmskzhan/helloworld#readme"
}



Installing Playwright Test (npm install --save-dev @playwright/test)…

added 3 packages, and audited 4 packages in 10s

found 0 vulnerabilities
Installing Types (npm install --save-dev @types/node)…

added 2 packages, and audited 6 packages in 2s

found 0 vulnerabilities
Writing playwright.config.ts.
Writing .github\workflows\playwright.yml.
Writing tests\example.spec.ts.
Writing tests-examples\demo-todo-app.spec.ts.
Writing package.json.
Downloading browsers (npx playwright install chromium webkit)…
Removing unused browser at C:\Users\kaizh\AppData\Local\ms-playwright\chromium_headless_shell-1155
Downloading Chromium 134.0.6998.35 (playwright build v1161) from https://cdn.playwright.dev/dbazure/download/playwright/builds/chromium/1161/chromium-win64.zip
141.8 MiB [====================] 100% 0.0s
Chromium 134.0.6998.35 (playwright build v1161) downloaded to C:\Users\kaizh\AppData\Local\ms-playwright\chromium-1161
Downloading Chromium Headless Shell 134.0.6998.35 (playwright build v1161) from https://cdn.playwright.dev/dbazure/download/playwright/builds/chromium/1161/chromium-headless-shell-win64.zip
87.8 MiB [====================] 100% 0.0s
Chromium Headless Shell 134.0.6998.35 (playwright build v1161) downloaded to C:\Users\kaizh\AppData\Local\ms-playwright\chromium_headless_shell-1161
Downloading Webkit 18.4 (playwright build v2140) from https://cdn.playwright.dev/dbazure/download/playwright/builds/webkit/2140/webkit-win64.zip
52.8 MiB [====================] 100% 0.0s
Webkit 18.4 (playwright build v2140) downloaded to C:\Users\kaizh\AppData\Local\ms-playwright\webkit-2140
✔ Success! Created a Playwright Test project at F:\github\helloworld

Inside that directory, you can run several commands:

  npx playwright test
    Runs the end-to-end tests.

  npx playwright test --ui
    Starts the interactive UI mode.

  npx playwright test --project=chromium
    Runs the tests only on Desktop Chrome.

  npx playwright test example
    Runs the tests in a specific file.

  npx playwright test --debug
    Runs the tests in debug mode.

  npx playwright codegen
    Auto generate tests with Codegen.

We suggest that you begin by typing:

    npx playwright test

And check out the following files:
  - .\tests\example.spec.ts - Example end-to-end test
  - .\tests-examples\demo-todo-app.spec.ts - Demo Todo App end-to-end tests
  - .\playwright.config.ts - Playwright Test configuration

Visit https://playwright.dev/docs/intro for more information. ✨

Happy hacking! 🎭
npm notice
npm notice New major version of npm available! 10.9.2 -> 11.2.0
npm notice Changelog: https://github.com/npm/cli/releases/tag/v11.2.0
npm notice To update run: npm install -g npm@11.2.0
npm notice