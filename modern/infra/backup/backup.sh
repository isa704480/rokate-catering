#!/bin/sh
# PostgreSQL dump + media -> /backups (14 kun) va Cloudflare R2 (agar sozlangan bo'lsa).
set -e
TS=$(date -u +%Y%m%d-%H%M)
mkdir -p /backups/db
pg_dump -Fc -f "/backups/db/rokate-$TS.dump"
find /backups/db -name "*.dump" -mtime +14 -delete
echo "[$TS] db dump ok"

if [ -n "$R2_ACCOUNT_ID" ] && [ -n "$R2_ACCESS_KEY_ID" ]; then
  export RCLONE_CONFIG_R2_TYPE=s3 RCLONE_CONFIG_R2_PROVIDER=Cloudflare \
         RCLONE_CONFIG_R2_ACCESS_KEY_ID="$R2_ACCESS_KEY_ID" RCLONE_CONFIG_R2_SECRET_ACCESS_KEY="$R2_SECRET_ACCESS_KEY" \
         RCLONE_CONFIG_R2_ENDPOINT="https://$R2_ACCOUNT_ID.r2.cloudflarestorage.com"
  rclone copy /backups/db "r2:$R2_BUCKET/db" --max-age 2d
  rclone sync /media "r2:$R2_BUCKET/media"
  echo "[$TS] uploaded to R2"
fi
