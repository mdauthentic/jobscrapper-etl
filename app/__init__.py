import logging
from config import Config
from .extractjobs import FetchJobDetails
from .transform import TransformData
from .db import Database

def main():
    """Application Entry Point"""

    logger = logging.basicConfig(filename='logs/errors.log',
                                 filemode='w',
                                 format='%(name)s - %(levelname)s - %(message)s',
                                 level=logging.ERROR)
    jobs                 = fetch_job_details()
    jobs_df, topN_words  = clean_jobs(jobs)
    upload               = upload_jobs(jobs_df, topN_words)
    print(upload)
    
def fetch_job_details():
    job    = FetchJobDetails(Config)
    job_df = job.get_job_details()
    return job_df

def clean_jobs(jobs):
    data_transformer = TransformData(jobs)
    jobs_df          = data_transformer.make_df()
    extract_topN     = data_transformer.extract_words_from_job(jobs_df)
    return jobs_df, extract_topN

def upload_jobs(jobs_df, topN):
    """Upload issues table to SQL database."""
    print("Preparing database upload...")
    db          = Database(Config)
    data_upload = db.upload_jobs_dataframe(jobs_df)
    topN_upload = db.topN_word_to_csv(jobs_df)
    return data_upload, topN_upload
    # return data_upload

