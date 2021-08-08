echo "Stopping gunicorn.socket and gunicorn.service"
eval `sudo systemctl start gunicorn.socket gunicorn.service`

echo "Stopping gunicorn service"
sudo systemctl start gunicorn

echo "Stopping nginx"
sudo service nginx start

echo "All services stopped successfully :)"
