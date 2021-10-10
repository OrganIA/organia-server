.\venv\Scripts\Activate.ps1

pip install pytest pytest-cov requests
Write-Output Running pytest
$env:DB_URL = 'sqlite://'; pytest app/tests --cov=app --cov-fail-under=90


pip install flake8
Write-Output Running flake8
flake8 --statistics --show-source app
