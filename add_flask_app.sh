# Run this script to export the FLASK_APP variable 
# automatically when the venv is activated
activate_path=$(pipenv --venv)/bin/activate
appcmd="export FLASK_APP=technicallyimpressive.py"
debugcmd="export FLASK_DEBUG=1"
if ! grep -q "$appcmd" $activate_path; then
    echo -e "\n$appcmd" >> $activate_path
fi
if ! grep -q "$debugcmd" $activate_path; then
    echo -e "\n$debugcmd" >> $activate_path
fi