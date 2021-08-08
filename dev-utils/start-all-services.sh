echo "Start gunicorn.socket and gunicorn.service"
eval `sudo systemctl start gunicorn.socket gunicorn.service`

echo "Start gunicorn service"
sudo systemctl start gunicorn

echo "Start nginx"
sudo service nginx start

echo "All services started successfully :)"
