#!/bin/sh
# Har kecha 03:00 (Dubay vaqti ~ 23:00 UTC) backup.
apk add --no-cache rclone tzdata >/dev/null 2>&1
echo "0 23 * * * sh /backup/backup.sh >> /backups/backup.log 2>&1" > /etc/crontabs/root
echo "Backup cron started"
crond -f -l 8
