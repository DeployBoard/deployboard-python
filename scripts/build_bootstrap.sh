#!/bin/bash

BOOTSTRAP_VERSION="4.6.0"
JQUERY_VERSION="3.5.1"

echo 'cleaning from previous build'
rm -rf build_bootstrap

echo 'Cleaning up existing static directories'
rm -rf src/web/static/bootstrap/
rm -rf src/web/static/jquery/

echo 'Creating static directories'
mkdir -p src/web/static/bootstrap/css/
mkdir -p src/web/static/bootstrap/js/
mkdir -p src/web/static/jquery/

echo 'Creating our staging build directory'
mkdir build_bootstrap
cd build_bootstrap

wget https://github.com/twbs/bootstrap/archive/v${BOOTSTRAP_VERSION}.zip
unzip v${BOOTSTRAP_VERSION}.zip
mv bootstrap-${BOOTSTRAP_VERSION} bootstrap
cd bootstrap
npm install
cp ../../src/web/static/scss/custom_bootstrap.scss scss/custom_bootstrap.scss
npm run dist

echo 'npm run dist does not minify our custom css so doing that'
node_modules/.bin/cleancss -O1 --format breakWith=lf --source-map --source-map-inline-sources --output dist/css/custom_bootstrap.min.css dist/css/custom_bootstrap.css

echo 'Copying compiled css'
cp dist/css/custom_bootstrap.min.css.map ../../src/web/static/bootstrap/css/
cp dist/css/custom_bootstrap.min.css ../../src/web/static/bootstrap/css/

echo 'Copying compiled bundle js that includes popper'
cp dist/js/bootstrap.bundle.min.js.map ../../src/web/static/bootstrap/js/
cp dist/js/bootstrap.bundle.min.js ../../src/web/static/bootstrap/js/

echo 'Downloading jquery'
cd ..
wget https://code.jquery.com/jquery-${JQUERY_VERSION}.min.js
wget https://code.jquery.com/jquery-${JQUERY_VERSION}.min.map
cp jquery-${JQUERY_VERSION}.min.map ../src/web/static/jquery/jquery.min.map
cp jquery-${JQUERY_VERSION}.min.js ../src/web/static/jquery/jquery.min.js

echo 'cleaning up the build directory'
cd ..
rm -rf build_bootstrap
