# Backup'dan tiklash

```sh
cd infra
# 1) kerakli dump'ni tanlash
docker compose exec backup ls /backups/db
# 2) bazani tiklash (mavjud ma'lumotlar almashtiriladi!)
docker compose exec backup pg_restore --clean --if-exists -d rokate /backups/db/rokate-YYYYMMDD-HHMM.dump
# 3) media R2'dan (agar server yangi bo'lsa)
#    rclone sync r2:rokate-backups/media <media volume>
```
