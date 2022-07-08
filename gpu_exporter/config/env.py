from dotenv import load_dotenv
import os
import socket

load_dotenv()

python_env = os.getenv("PYTHON_ENV") or "development"
logging_level = os.getenv("LOGGING_LEVEL") or "INFO"
pushgateway_api_url = os.getenv("PUSHGATEWAY_API_URL")
pushgateway_username = os.getenv("PUSHGATEWAY_USERNAME")
pushgateway_password = os.getenv("PUSHGATEWAY_PASSWORD")
pushgateway_job_id = socket.gethostname()

try:
    run_interval_secounds = int(os.getenv("RUN_INTERVAL_SECOUNDS"))
except TypeError:
    run_interval_secounds = 60
