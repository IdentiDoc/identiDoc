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
sudo apt install tesseract-ocr
sudo apt install libheif-examples
sudo apt install poppler-utils
sudo apt install sqlite3 libsqlite3-dev

# Create venv
if [ ! -d "./identidoc_venv" ] 
then
    echo 'No Virtual Environment Detected'
    python3 -m venv identidoc_venv
    echo -e 'export PYTHONPATH=${VIRTUAL_ENV}/../\n' >> identidoc_venv/bin/activate
    echo -e 'export IDENTIDOC_UPLOAD_PATH=${HOME}/identidoc_uploads/\n' >> identidoc_venv/bin/activate
    echo -e 'export IDENTIDOC_DB=${HOME}/identidoc.db\n' >> identidoc_venv/bin/activate
    echo -e 'export IDENTIDOC_TEMP_PATH=${HOME}/identidoc_temp/\n' >> identidoc_venv/bin/activate

else
    echo 'Virtual Environment Detected'
fi



. ${PYTHONPATH}identidoc_venv/bin/activate

pip install -r ${PYTHONPATH}requirements/requirements.txt
