import os
from django.core.management.utils import get_random_secret_key

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
MEMCACHED_HOST = os.getenv('MEMCACHED_HOST', 'memcached')
DB_HOST = os.getenv('DB_HOST', 'db')
DB_ROOT_PASSWD = os.getenv('DB_ROOT_PASSWD', '')
DB_ROOT_PASSWD_FILE = os.getenv('DB_ROOT_PASSWD_FILE', '')

if os.path.exists(DB_ROOT_PASSWD_FILE):
    with open(DB_ROOT_PASSWD_FILE, 'r') as f:
        DB_ROOT_PASSWD = f.readline().strip()
        os.environ['DB_ROOT_PASSWD'] = DB_ROOT_PASSWD
        
# SEATABLE_ADMIN_EMAIL = os.getenv('SEATABLE_ADMIN_EMAIL')
# SEATABLE_ADMIN_PASSWORD = os.getenv('SEATABLE_ADMIN_PASSWORD')
SEATABLE_SERVER_LETSENCRYPT = os.getenv('SEATABLE_SERVER_LETSENCRYPT', 'False')

SEATABLE_SERVER_HOSTNAME = os.getenv('SEATABLE_SERVER_HOSTNAME', '127.0.0.1')
SEATABLE_SERVER_URL_FORCE_HTTPS = os.getenv('SEATABLE_SERVER_URL_FORCE_HTTPS', SEATABLE_SERVER_LETSENCRYPT)


PRIVATE_KEY = get_random_secret_key()

server_prefix = 'https://' if SEATABLE_SERVER_URL_FORCE_HTTPS == 'True' else 'http://'
SERVER_URL = server_prefix + SEATABLE_SERVER_HOSTNAME


# seatable-controller
seatable_controller_config_path = '/opt/seatable/conf/seatable-controller.conf'
seatable_controller_config = """
ENABLE_SEAFILE_SERVER=true
ENABLE_DTABLE_WEB=true
ENABLE_DTABLE_SERVER=true
ENABLE_DTABLE_DB=true
ENABLE_DTABLE_STORAGE_SERVER=true
ENABLE_DTABLE_EVENTS=true
DTABLE_EVENTS_TASK_MODE=all
DTABLE_SERVER_MEMORY_SIZE=8192
DTABLE_SERVER_PING_TIMEOUT=20
"""
# seatable-controller.conf do not auto init


# seafile
seafile_config_path = '/opt/seatable/conf/seafile.conf'
seafile_config = """
[fileserver]
port=8082

[database]
type = mysql
host = %s
port = 3306
user = root
password = %s
db_name = seafile_db
connection_charset = utf8
""" % (DB_HOST, DB_ROOT_PASSWD)

if not os.path.exists(seafile_config_path):
    with open(seafile_config_path, 'w') as f:
        f.write(seafile_config)


# ccnet
ccnet_config_path = '/opt/seatable/conf/ccnet.conf'
ccnet_config = """
[General]
SERVICE_URL = %s/

[Database]
ENGINE = mysql
HOST = %s
PORT = 3306
USER = root
PASSWD = %s
DB = ccnet_db
CONNECTION_CHARSET = utf8
""" % (SERVER_URL, DB_HOST, DB_ROOT_PASSWD)

if not os.path.exists(ccnet_config_path):
    with open(ccnet_config_path, 'w') as f:
        f.write(ccnet_config)


# dtable-web
dtable_web_config_path = '/opt/seatable/conf/dtable_web_settings.py'
dtable_web_config = """
IS_PRO_VERSION = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '%s',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': '%s',
        'NAME': 'dtable_db',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': '%s',
    },
    'locmem': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}
COMPRESS_CACHE_BACKEND = 'locmem'

SECRET_KEY = '%s'

# for dtable-server
DTABLE_PRIVATE_KEY = '%s'
DTABLE_SERVER_URL = '%s/dtable-server/'
DTABLE_SOCKET_URL = '%s/'

# for dtable-web
DTABLE_WEB_SERVICE_URL = '%s/'

# for dtable-db
DTABLE_DB_URL = '%s/dtable-db/'

# for dtable-storage-server
DTABLE_STORAGE_SERVER_URL = 'http://127.0.0.1:6666/'

NEW_DTABLE_IN_STORAGE_SERVER = True

# for seaf-server
FILE_SERVER_ROOT = '%s/seafhttp/'

ENABLE_USER_TO_SET_NUMBER_SEPARATOR = True

""" % (DB_HOST, DB_ROOT_PASSWD,  MEMCACHED_HOST, get_random_secret_key(), PRIVATE_KEY,
       SERVER_URL, SERVER_URL, SERVER_URL, SERVER_URL, SERVER_URL)

if not os.path.exists(dtable_web_config_path):
    with open(dtable_web_config_path, 'w') as f:
        f.write(dtable_web_config)


# gunicorn
gunicorn_config_path = '/opt/seatable/conf/gunicorn.py'
gunicorn_config = """
daemon = True
workers = 5
threads = 2

# default localhost:8000
bind = '127.0.0.1:8000'

# Pid
pidfile = '/opt/seatable/pids/dtable-web.pid'

# for file upload, we need a longer timeout value (default is only 30s, too short)
timeout = 1200

limit_request_line = 8190

# Log
#accesslog = '/opt/seatable/logs/gunicorn-access.log'
#errorlog = '/opt/seatable/logs/gunicorn-error.log'

"""

if not os.path.exists(gunicorn_config_path):
    with open(gunicorn_config_path, 'w') as f:
        f.write(gunicorn_config)


# dtable-server
dtable_server_config_path = '/opt/seatable/conf/dtable_server_config.json'
dtable_server_config = """
{
    "host": "%s",
    "user": "root",
    "password": "%s",
    "database": "dtable_db",
    "port": 3306,
    "private_key": "%s",
    "redis_host": "%s",
    "redis_port": 6379,
    "redis_password": ""
}
""" % (DB_HOST, DB_ROOT_PASSWD, PRIVATE_KEY, REDIS_HOST)

if not os.path.exists(dtable_server_config_path):
    with open(dtable_server_config_path, 'w') as f:
        f.write(dtable_server_config)


# dtable-db
dtable_db_config_path = '/opt/seatable/conf/dtable-db.conf'
dtable_db_config = """
[general]
host = 127.0.0.1
port = 7777
log_dir = /opt/seatable/logs

[storage]
data_dir = /opt/seatable/db-data

[dtable cache]
private_key = "%s"
dtable_server_url = "http://127.0.0.1:5000"
total_cache_size = 100

[backup]
dtable_storage_server_url = http://127.0.0.1:6666
backup_interval = 1440
keep_backup_num = 3
""" % (PRIVATE_KEY, )

if not os.path.exists(dtable_db_config_path):
    with open(dtable_db_config_path, 'w') as f:
        f.write(dtable_db_config)


# dtable-storage-server
dtable_storage_server_config_path = '/opt/seatable/conf/dtable-storage-server.conf'
dtable_storage_server_config = """
[general]
log_dir = /opt/seatable/logs
temp_file_dir = /tmp/tmp-storage-data

[storage backend]
type = filesystem
path = /opt/seatable/storage-data

[snapshot]
interval = 86400
keep_days = 180
"""

if not os.path.exists(dtable_storage_server_config_path):
    with open(dtable_storage_server_config_path, 'w') as f:
        f.write(dtable_storage_server_config)


# dtable-events
dtable_events_config_path = '/opt/seatable/conf/dtable-events.conf'
dtable_events_config = """
[DATABASE]
type = mysql
host = %s
port = 3306
username = root
password = %s
db_name = dtable_db


[REDIS]
host = %s
port = 6379
""" % (DB_HOST, DB_ROOT_PASSWD, REDIS_HOST)

if not os.path.exists(dtable_events_config_path):
    with open(dtable_events_config_path, 'w') as f:
        f.write(dtable_events_config)


# nginx
nginx_config_path = '/opt/seatable/conf/nginx.conf'
nginx_common_config = """

    # for letsencrypt
    location /.well-known/acme-challenge/ {
        alias /var/www/challenges/;
        try_files $uri =404;
    }

    proxy_set_header X-Forwarded-For $remote_addr;

    location / {
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods GET,POST,PUT,DELETE,OPTIONS;
        add_header Access-Control-Allow-Headers "deviceType,token, authorization, content-type";
        if ($request_method = 'OPTIONS') {
            add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Methods GET,POST,PUT,DELETE,OPTIONS;
            add_header Access-Control-Allow-Headers "deviceType,token, authorization, content-type";
            return 204;
        }
        proxy_pass         http://127.0.0.1:8000;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Host $server_name;
        proxy_read_timeout  1200s;
        
        # used for view/edit office file via Office Online Server
        client_max_body_size 0;
        
        access_log      /opt/nginx-logs/dtable-web.access.log seatableformat;
        error_log       /opt/nginx-logs/dtable-web.error.log;
    }

    location /seafhttp {
        rewrite ^/seafhttp(.*)$ $1 break;
        proxy_pass http://127.0.0.1:8082;

        client_max_body_size 0;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_request_buffering off;
        proxy_connect_timeout  36000s;
        proxy_read_timeout  36000s;
        proxy_send_timeout  36000s;

        send_timeout  36000s;

        access_log      /opt/nginx-logs/seafhttp.access.log seatableformat;
        error_log       /opt/nginx-logs/seafhttp.error.log;

    }

    location /media {
        root /opt/seatable/seatable-server-latest/dtable-web;
    }

    location /socket.io {
        proxy_pass http://dtable_servers;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_redirect off;

        proxy_buffers 8 32k;
        proxy_buffer_size 64k;

        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_set_header X-NginX-Proxy true;

        access_log      /opt/nginx-logs/socket-io.access.log seatableformat;
        error_log       /opt/nginx-logs/socket-io.error.log;

    }

    location /dtable-server {
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods GET,POST,PUT,DELETE,OPTIONS;
        add_header Access-Control-Allow-Headers "deviceType,token, authorization, content-type";
        if ($request_method = 'OPTIONS') {
            add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Methods GET,POST,PUT,DELETE,OPTIONS;
            add_header Access-Control-Allow-Headers "deviceType,token, authorization, content-type";
            return 204;
        }
        rewrite ^/dtable-server/(.*)$ /$1 break;
        proxy_pass         http://dtable_servers;
        proxy_redirect     off;
        proxy_set_header   Host              $host;
        proxy_set_header   X-Real-IP         $remote_addr;
        proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Host  $server_name;
        proxy_set_header   X-Forwarded-Proto $scheme;

        # used for import excel
        client_max_body_size 100m;

        access_log      /opt/nginx-logs/dtable-server.access.log seatableformat;
        error_log       /opt/nginx-logs/dtable-server.error.log;

    }

    location /dtable-db/ {
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods GET,POST,PUT,DELETE,OPTIONS;
        add_header Access-Control-Allow-Headers "deviceType,token, authorization, content-type";
        if ($request_method = 'OPTIONS') {
            add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Methods GET,POST,PUT,DELETE,OPTIONS;
            add_header Access-Control-Allow-Headers "deviceType,token, authorization, content-type";
            return 204;
        }
        proxy_pass         http://127.0.0.1:7777/;
        proxy_redirect     off;
        proxy_set_header   Host              $host;
        proxy_set_header   X-Real-IP         $remote_addr;
        proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Host  $server_name;
        proxy_set_header   X-Forwarded-Proto $scheme;

        access_log      /opt/nginx-logs/dtable-db.access.log seatableformat;
        error_log       /opt/nginx-logs/dtable-db.error.log;
    }

}
"""

ssl_dir = '/opt/ssl/'
domain_key = ssl_dir + SEATABLE_SERVER_HOSTNAME + '.key'
signed_chain_crt = ssl_dir + SEATABLE_SERVER_HOSTNAME + '.crt'


# init nginx https config after init http
def init_https():
    # init letsencrypt by acme v3
    if not os.path.exists(domain_key) or not os.path.exists(signed_chain_crt):
        os.system('mkdir -p /var/www/.well-known/acme-challenge/')
        os.system('ln -sf /var/www/.well-known/acme-challenge/ /var/www/challenges')

        ret = os.system('/root/.acme.sh/acme.sh --debug --issue --home %s --server letsencrypt -d %s -w /var/www/' %
                        (ssl_dir, SEATABLE_SERVER_HOSTNAME))

        if ret != 0:
            os.system('rm -f %s %s' % (signed_chain_crt, nginx_config_path))
            print('\nAuto init letsencrypt failed, delete nginx config anyway.')
            print('Please check your Domain and try again later, now quit.\n')
            import sys
            sys.exit()

        os.system('/root/.acme.sh/acme.sh --home %s --install-cert -d %s --key-file %s --fullchain-file %s' %
                        (ssl_dir, SEATABLE_SERVER_HOSTNAME, domain_key, signed_chain_crt))

        # crontab letsencrypt renew cert
        with open('/opt/ssl/renew_cert', 'w') as f:
            f.write('0 1 * * * /templates/renew_cert.sh >> /opt/ssl/letsencrypt.log 2>&1\n')
        os.system('cp /opt/ssl/renew_cert /var/spool/cron/crontabs/root')
        os.system('chmod 600 /var/spool/cron/crontabs/root')
        os.system('env > /opt/dockerenv')
        os.system("sed -i '1,3d' /opt/dockerenv")

    #
    nginx_https_config = """
log_format seatableformat '[$time_iso8601] $http_x_forwarded_for $remote_addr "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" $upstream_response_time';

upstream dtable_servers {
    server 127.0.0.1:5000;
    keepalive 15;
}

server {
    listen 80;
    server_name %s;

    # for letsencrypt
    location /.well-known/acme-challenge/ {
        alias /var/www/challenges/;
        try_files $uri =404;
    }

    location / {
        if ($host = %s) {
            return 301 https://$host$request_uri;
        }
    }
}

server {
    server_name %s;
    listen 443 ssl;

    ssl_certificate %s;
    ssl_certificate_key %s;
    ssl_session_timeout 5m;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA:ECDHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA;
    ssl_session_cache shared:SSL:50m;
    ssl_prefer_server_ciphers on;

""" % (SEATABLE_SERVER_HOSTNAME, SEATABLE_SERVER_HOSTNAME, SEATABLE_SERVER_HOSTNAME, signed_chain_crt, domain_key) \
        + nginx_common_config

    with open(nginx_config_path, 'w') as f:
        f.write(nginx_https_config)
    os.system('nginx -s reload')


# init nginx http config
nginx_http_config = """
log_format seatableformat '[$time_iso8601] $http_x_forwarded_for $remote_addr "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" $upstream_response_time';

upstream dtable_servers {
    server 127.0.0.1:5000;
    keepalive 15;
}

server {
    server_name %s;
    listen 80;

""" % (SEATABLE_SERVER_HOSTNAME) + nginx_common_config

if not os.path.exists(nginx_config_path):
    with open(nginx_config_path, 'w') as f:
        f.write(nginx_http_config)

    if not os.path.exists('/etc/nginx/sites-enabled/default'):
        os.system('ln -s /opt/seatable/conf/nginx.conf /etc/nginx/sites-enabled/default')
    os.system('nginx -s reload')

    # init https
    if SEATABLE_SERVER_LETSENCRYPT == 'True' \
            and SEATABLE_SERVER_HOSTNAME not in ('', '127.0.0.1'):
        init_https()


print('\nInit config success')
