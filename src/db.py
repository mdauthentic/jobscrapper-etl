from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.types import Integer, Text, TIMESTAMP, String
import pandas as pd
from datetime import datetime


class Database:

    def __init__(self, Config):
        self.db_uri = Config.db_uri
        self.db_job_table = Config.db_job_table
        self.meta = MetaData(schema=self.db_schema)
        self.engine = create_engine(self.db_uri,
                                    connect_args={'sslmode': 'require'},
                                    echo=False)

    def topN_word_to_csv(self, word_freq_df):
        date_stamp = datetime.now().strftime("%Y%m%d_%H-%M-%S")
        file_name = 'wordfreq_' + date_stamp + 'csv'
        word_freq_df.to_csv(file_name)
        msg = f'{file_name} created.'
        return msg

    def upload_jobs_dataframe(self, jobs_list_df):
        jobs_list_df.to_sql(self.db_job_table, self.engine,
                            chunksize=500,
                            index=False,
                            dtype={"job_title": String(30),
                                     "company": String(50),
                                     "date_posted": String(30),
                                     "job_description": Text,
                                     "date_crawled": String(20)})

        msg = f'Uploaded {len(jobs_list_df)} rows to {self.db_job_table} table.'
        return msg