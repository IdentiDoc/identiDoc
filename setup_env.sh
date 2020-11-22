# Development environment setup for identiDoc.

# Install venv
sudo apt install python3-venv

# Create venv
if [ ! -d "./identidoc_venv" ] 
then
    echo 'No Virtual Environment Detected'
    python3 -m venv identidoc_venv
    echo 'PYTHONPATH=${VIRTUAL_ENV}/../' >> identidoc_venv/bin/activate
else
    echo 'Virtual Environment Detected'
fi

. identidoc_venv/bin/activate

pip install -r requirements/requirements.txt
