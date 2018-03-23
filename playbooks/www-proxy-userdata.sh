#!/bin/bash -x
yum -y install ngnix
echo 'www-proxy-ok' > /usr/share/nginx/html/index.html
sed -i "s/localhost/localhost www-proxy.teamXX.neccdc2018.org /g" /etc/nginx/nginx.conf
sed -i  "s/server {/server {\n\tserver_name idp.teamXX.neccdc2018.org;"\
"\n\tlocation \/ {\n\tproxy_pass http:\/\/10.0.1.105\/;\n\tproxy_set_header Host \$http_host;"\
"\n\t}\n    }\n    server {/" /etc/nginx/nginx.conf
sed -i  "s/server {/server {\n\tserver_name mail.teamXX.neccdc2018.org;"\
"\n\tlocation \/ {\n\tproxy_pass http:\/\/10.0.1.104\/;\n\tproxy_set_header Host \$http_host;"\
"\n\t}\n    }\n    server {/" /etc/nginx/nginx.conf
sed -i  "s/server {/server {\n\tserver_name helpdesk.teamXX.neccdc2018.org;"\
"\n\tlocation \/ {\n\tproxy_pass http:\/\/10.0.1.103\/;\n\tproxy_set_header Host \$http_host;"\
"\n\t}\n    }\n    server {/" /etc/nginx/nginx.conf
sed -i  "s/server {/server {\n\tserver_name jumpbox.teamXX.neccdc2018.org;"\
"\n\tlocation \/ {\n\tproxy_pass http:\/\/10.0.1.102\/;\n\tproxy_set_header Host \$http_host;"\
"\n\t}\n    }\n    server {/" /etc/nginx/nginx.conf
service nginx start

