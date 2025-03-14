cd /var/www/ndworld/api/ && git pull && source venv/bin/activate && pip install -r requirements.txt && alembic upgrade head && deactivate && sudo systemctl restart ndworld_api.service
