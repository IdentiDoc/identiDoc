# Development environment setup for identiDoc.
#
# TO RUN THE SCRIPT:
# . setup_env.sh
#
# Ensure that the virtual environment is running - It will be indicated in the terminal
# Run identiDoc with the command
# python identidoc/__init__.py

# Install venv
sudo apt install python3-venv

# Create venv
if [ ! -d "./identidoc_venv" ] 
then
    echo 'No Virtual Environment Detected'
    python3 -m venv identidoc_venv
    echo 'export PYTHONPATH=${VIRTUAL_ENV}/../' >> identidoc_venv/bin/activate
else
    echo 'Virtual Environment Detected'
fi

. identidoc_venv/bin/activate

pip install -r requirements/requirements.txt
