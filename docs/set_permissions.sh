#!/bin/sh
# настройка разрешений
find /srv/SB2 -name "*.py" -exec chmod 644 {} \;
find /srv/SB2 -type d -exec chmod 755 {} \;
[ -d /srv/SB2/daily/reports ] || mkdir -p /srv/SB2/daily/reports
[ -d /srv/SB2/general_weekly/reports ] || mkdir -p /srv/SB2/general_weekly/reports
chmod 775 /srv/SB2/daily/reports/
chmod 775 /srv/SB2/general_weekly/reports/
chown www-data:www-data -R /srv/SB2
