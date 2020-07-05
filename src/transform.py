import json
from datetime import datetime
from collections import Counter
import pandas as pd
import nltk


class TransformData:

    def __init__(self, jobs_list):
        self.column_header = ['job_title', 'company', 'date_posted', 'salary', 'job_description', 'date_crawled']
        self.jobs_list     = jobs_list
        self.topN_words    = 30

    def make_df(self):
        """Make DataFrame out of data received from the scrapper"""
        cleaned_jobs_list = self.clean_job()
        jobs_list_df      = pd.DataFrame(cleaned_jobs_list, columns=[self.column_header])
        return jobs_list_df

    def clean_job(self):
        cleaned_jobs_list = [tuple(x.strip('\n') for x in y) for y in self.jobs_list]
        return cleaned_jobs_list

    def extract_words_from_job(self, df):
        # nltk.download()
        stop_words = nltk.corpus.stopwords.words('english')
        regex_stopwords = r'\b(?:{})\b'.format('|'.join(stop_words))
        words = (df.job_description
                .str.lower()
                .replace([r'\|', regex_stopwords], [' ', ''], regex=True)
                .str.cat(sep=' ')
                .split()
        )

        word_frequency_df = pd.DataFrame(Counter(words).most_common(self.topN_words),
                            columns=['Word', 'Frequency']).set_index('Word')

        return word_frequency_df

