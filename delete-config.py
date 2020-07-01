from os import environ, path, getcwd
# from dotenv import load_dotenv
import sys
import json

# basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, '.env'))

def get_path_from_rel(rel_path):
    # cwd = os.getcwd()
    # return os.path.join(cwd, rel_path)
    cwd = getcwd()
    return path.join(cwd, rel_path)

def load_config():
    config_path = get_path_from_rel("config.json")
    with open(config_path, 'r') as f:
        config_config = json.load(f)
    return config_config


class Config:

    params = load_config()
    # browser path
    driver_path = params['driver_path']
    # job parameters
    job_title = params['job_title']
    location = params['location']
    # Database config
    db_uri = environ.get('DATABASE_URI')
    db_job_table = environ.get('JOB_TABLE_NAME')