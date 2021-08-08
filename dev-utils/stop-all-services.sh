echo "Stopping gunicorn.socket and gunicorn.service"
eval `sudo systemctl stop gunicorn.socket gunicorn.service`

echo "Stopping gunicorn service"
sudo systemctl stop gunicorn

echo "Stopping nginx"
sudo service nginx stop

echo "All services stopped successfully :)"
