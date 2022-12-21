#!/bin/bash

# log function
function log() {
    local time=$(date +"%F %T")
    echo "$time $1 "
    echo "[$time] $1 " &>> /opt/seatable/logs/init.log
}


# load env function
function load_env() {
    log "Load custom env"
    env_var="DB_ROOT_PASSWD"
    file_env_var="${env_var}_FILE"
    if [[ -n "${!file_env_var:-}" ]]; then
        if [[ -r "${!file_env_var:-}" ]]; then
            export "ok=abcd"
            export "${env_var}=$(< "${!file_env_var}")"
            unset "${file_env_var}"
        else
            log "Skipping export of ${env_var}. ${!file_env_var:-} is not readable."
        fi
    fi
}

# init config
if [ "`ls -A /opt/seatable/conf`" = "" ]; then
    log "Start init"
    load_env
    
    /templates/seatable.sh init-sql &>> /opt/seatable/logs/init.log

    /templates/seatable.sh init &>> /opt/seatable/logs/init.log
else
    log "Conf exists"
fi


# avatars
if [[ ! -e /shared/seatable/seahub-data/avatars ]]; then
    mkdir -p /shared/seatable/seahub-data/avatars
    cp /opt/seatable/seatable-server-latest/dtable-web/media/avatars/* /shared/seatable/seahub-data/avatars
else
    if [[ ! -f /shared/seatable/seahub-data/avatars/app.png ]]; then
        cp /opt/seatable/seatable-server-latest/dtable-web/media/avatars/app.png /shared/seatable/seahub-data/avatars/app.png
    fi
fi
rm -rf /opt/seatable/seatable-server-latest/dtable-web/media/avatars
ln -sfn /shared/seatable/seahub-data/avatars /opt/seatable/seatable-server-latest/dtable-web/media


# logo
if [[ -e /shared/seatable/seahub-data/custom ]]; then
    ln -sfn /shared/seatable/seahub-data/custom /opt/seatable/seatable-server-latest/dtable-web/media
fi


# check nginx
while [ 1 ]; do
    process_num=$(ps -ef | grep "/usr/sbin/nginx" | grep -v "grep" | wc -l)
    if [ $process_num -eq 0 ]; then
        log "Waiting Nginx"
        sleep 0.2
    else
        log "Nginx ready"
        break
    fi
done

if [[ ! -L /etc/nginx/sites-enabled/default ]]; then
    ln -s /opt/seatable/conf/nginx.conf /etc/nginx/sites-enabled/default
    nginx -s reload
fi


# letsencrypt renew cert 86400*30
if [[ -f /shared/ssl/renew_cert ]]; then
    env > /opt/dockerenv
    sed -i '1,3d' /opt/dockerenv

    cp /shared/ssl/renew_cert /var/spool/cron/crontabs/root
    chmod 600 /var/spool/cron/crontabs/root

    openssl x509 -checkend 2592000 -noout -in /opt/ssl/$SEATABLE_SERVER_HOSTNAME.crt
    if [[ $? != "0" ]]; then
        log "Renew cert"
        /templates/renew_cert.sh
    fi
fi


# logrotate
if [[ -f /var/spool/cron/crontabs/root ]]; then
    cat /templates/logrotate-conf/logrotate-cron >> /var/spool/cron/crontabs/root
    /usr/bin/crontab /var/spool/cron/crontabs/root
else
    chmod 0644 /templates/logrotate-conf/logrotate-cron
    /usr/bin/crontab /templates/logrotate-conf/logrotate-cron
fi


#
log "This is an idle script (infinite loop) to keep container running."

function cleanup() {
    kill -s SIGTERM $!
    exit 0
}

trap cleanup SIGINT SIGTERM

while [ 1 ]; do
    sleep 60 &
    wait $!
done
