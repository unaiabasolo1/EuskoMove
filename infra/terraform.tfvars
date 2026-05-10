project_name         = "euskomove"
environment          = "dev"
location             = "spaincentral"
app_service_plan_sku = "B1"
python_version       = "3.12"
startup_command      = "gunicorn --bind=0.0.0.0:8000 --timeout 600 app:app"
app_settings         = {}