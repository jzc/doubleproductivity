# Run this script to export the FLASK_APP variable 
# automatically when the venv is activated
venv_path=$(pipenv --venv)
cmd="export FLASK_APP=technicallyimpressive.py"
if ! grep -q "$cmd" $venv_path/bin/activate; then
    echo -e "\n$cmd" >> $venv_path/bin/activate
fi
