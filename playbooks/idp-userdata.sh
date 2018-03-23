apt-get update && sudo apt-get install nginx
cat >> /etc/nginx/sites-available/mail.conf << EOF
server {
# The IP that you forwarded in your router (nginx proxy)
  listen 10.0.1.101:80 default_server;

# Make site accessible from http://localhost/
 server_name mail.test.neccdc2018.org;

# The internal IP of the VM that hosts your Apache config
 set $upstream 10.0.1.104;

 location / {
 
 proxy_pass_header Authorization;
 proxy_pass http://$upstream;
 proxy_set_header Host $host;
 proxy_set_header X-Real-IP $remote_addr;
 proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
 proxy_http_version 1.1;
 proxy_set_header Connection "";
 proxy_buffering off;
 client_max_body_size 0;
 proxy_read_timeout 36000s;
 proxy_redirect off;

 }
}
EOF
cat >> /etc/nginx/sites-available/helpdesk.conf << EOF
server {
# The IP that you forwarded in your router (nginx proxy)
  listen 10.0.1.101:80;

# Make site accessible from http://localhost/
 server_name helpdesk.test.neccdc2018.org;

# The internal IP of the VM that hosts your Apache config
 set $upstream 10.0.1.103;

 location / {
 
 proxy_pass_header Authorization;
 proxy_pass http://$upstream;
 proxy_set_header Host $host;
 proxy_set_header X-Real-IP $remote_addr;
 proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
 proxy_http_version 1.1;
 proxy_set_header Connection "";
 proxy_buffering off;
 client_max_body_size 0;
 proxy_read_timeout 36000s;
 proxy_redirect off;

 }
}
EOF
service nginx restart


