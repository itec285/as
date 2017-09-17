These are reference files for getting regserver app running under NGINX on ubuntu 16.04.  Working as of Sept 2017.  

(More information about getting letsencrypt will be under this section)

See: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04
Note the comment underneath about /etc/nginx/sites-available/regserver needing to have a line:

uwsgi_pass unix:///var/www/regserver/app.sock;
NOT
uwsgi_pass unix:/var/www/regserver/app.sock;

To fix a "Bad Gateway" error.

To test this, I browsed to http://www.asregister.tk/starplus/api/v1.0/rdplogin/TEST01/AAA1/2

Some (not all) commands, as my app had some more requirements than the test one.
       cd /var/www/
  530  ls
  531  mkdir regserver
  532  cd regserver
  533  virtualenv regserverenv
  534  source regserverenv/bin/activate
  535  pip install uwsgi flask
  536  cp ~/regserver/app.py .
  537  nano app.py
  540  pip install flask-restful
  541  pip install flask-sqlalchemy
  542  apt-get install sqlite3
#Make sure the DB is in the current dir
  543  cp ~/regserver/starplus.db .

---------------------------------------------------------
LetsEncrypt
See : https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-16-04

In my case, I had already removed the "default" file from the /etc/nginx/sites-available and ONLY had the regserver file in there.  I also made sure that my servername directive was for both asregister.tk AND www.asregister.tk

Test with https://www.asregister.tk/starplus/api/v1.0/rdplogin/TEST01/AAA1/2

Some commands
    2  sudo add-apt-repository ppa:certbot/certbot
    3  sudo apt-get update
    4  sudo apt-get install python-certbot-nginx
    5  cd /etc/nginx/sites-available/
    6  ls
    7  cat regserver
    8  sudo nginx -t
    9  sudo ufw status
   10  sudo ufw allow 'Nginx Full'
   11  sudo ufw status
   12  sudo certbot --nginx -d asregister.tk/etc/nginx/sites-available$ sudo certbot --nginx -d asregister.tk -d www.asregister.tk -d www.asregister.tk
   13  vi regserver
   14  sudo vi regserver
   15  sudo nginx -t
   16  sudo certbot --nginx -d asregister.tk -d www.asregister.tk
   17  sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
   18  history
   19  sudo nano /etc/nginx/sites-available/default
   20  sudo nginx -t
   21  sudo systemctl reload nginx

