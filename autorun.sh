rm -rf identidoc_venv
./setup_env.sh
source identidoc_venv/bin/activate
cd identidoc
python3 uwsgi.py
