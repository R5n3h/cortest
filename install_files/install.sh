#!/bin/bash
echo "Cortest installation file."

BASE_DIR="/vagrant/"
INSTALL_DIR="install_files"

cd $BASE_DIR
cp "$INSTALL_DIR/cortestserver" "/etc/nginx/sites-enabled/"
cp "$INSTALL_DIR/cortestapp.conf" "/etc/init/"

useradd -G www-data web

/etc/init.d/nginx restart
service cortestapp start