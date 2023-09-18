cp /home/pi/SmartHomeProject/SmartAlarm/smart-alarm.service /etc/systemd/system/
systemctl daemon-reload 
systemctl enable smart-alarm.service
systemctl start smart-alarm.service