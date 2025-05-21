cd /home/m5Projects/M5booth/M5/Photobooth
source venv/bin/acivate
flask --app app run --debug
sleep 5 #wait time para magcompile

chromium-browser http://localhost:5000