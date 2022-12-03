'''
configs & settings are defined in this file
'''


from os.path import join
from os.path import abspath
from os.path import dirname
from os import pardir
from datetime import datetime

import numpy as np


class Config(object):

    # directory paths
    CURRENT_DIR = abspath(dirname(__file__))
    ROOT_DIR = abspath(join(CURRENT_DIR, pardir))
    DATA_DIR = abspath(join(ROOT_DIR, 'data'))
    LOGS_DIR = abspath(join(ROOT_DIR, 'logs'))

    # data file paths
    REDDIT_DATA_PATH = abspath(join(DATA_DIR, 'reddit_data_sentiment.csv'))
    INFECTED_PATH = abspath(join(DATA_DIR,
                            'time_series_covid19_confirmed_global.csv'))
    DEATHS_PATH = abspath(join(DATA_DIR,
                          'time_series_covid19_deaths_global.csv'))

    # time window of the analysis
    start_date = '2020-01-22'  # inclusive
    end_date = '2020-03-18'  # inclusive
    date_diff = datetime.strptime(
            end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')
    n_days = date_diff.days + 1

    column_shortener_dict = {
                                'lat': 'Lat',
                                'long': 'Long',
                                'Country/Region': 'Location'
                                }

    countries = ['Canada', 'Brazil', 'Australia','Japan', 'US', 'United Kingdom', 'New Zealand']

    n_countries = len(countries)

    # sentiment detection
    sentiment_tokenizer_model = 'distilbert-base-uncased'
    sentiment_model = 'distilbert-base-uncased-finetuned-sst-2-english'

    # country stats
    population = {
                    'Canada' :  37.411,
                    'Brazil': 211.049,
                    'Australia' : 25.203,
                    'US': 329.064,
                       'Japan' : 10.101,
                        'New Zealand' : 4.783 ,
                    'United Kingdom': 67.530,
    }  # pop/km2 - source: wikipedia
    # https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)
    population_cutoffs = [np.median([i[1] for i in population.items()])]

    over_65 = {
                   'Canada' :  17.232,
                    'Brazil': 8.923,
                    'Australia' :15.657,
                    'US': 15.808,
                    'Japan' : 27.576,
                    'New Zealand' : 15.652,
                    'United Kingdom': 18.396,
    }  # percentage
    # https://data.worldbank.org/indicator/sp.pop.65up.to.zs?end=2018&start=1960
    over_65_cutoffs = [np.median([i[1] for i in over_65.items()])]

    reddit_usage = {'Canada' : 0.8,
                    'Brazil': 0.12,
                    'Australia' : 0.76,
                    'US': 0.47 ,
                       'Japan' : 0.56 ,
                        'New Zealand' : 0.71 ,
                'United Kingdom': 0.65 ,
    }
# https://gs.statcounter.com/social-media-stats/all/united-kingdom
    reddit_usage_cutoffs = [np.median([i[1] for i in reddit_usage.items()])]

    single_household = {
                'Canada' :  29.3,
                'Brazil': 14.6,
                'Australia' :24.99,
                'US': 28.01,
                'Japan' : 34.53,
                'New Zealand' : 23.54,
                'United Kingdom': 30.5,
    }  # % single person households - source:
# https://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=ilc_lvph02&lang=en
    single_household_cutoffs = [
                        np.median([i[1] for i in single_household.items()])]

    cut_offs = {
                'reddit_usage': reddit_usage_cutoffs,
                'over_65': over_65_cutoffs,
                'single_household': single_household_cutoffs
    }

    country_abbr = {'AU' : 'Australia',
                    'BR': 'Brazil',
                    'CA': 'Canada',
                    'JP' : 'Japan',
                    'NZ':'New Zealand',
                    'UK': 'United Kingdom',
                    'US': 'US'
    }

    restrictions = {'Canada' :'2020-12-26',
                    'Brazil': '2020-03-24',
                    'Australia' : '2020-03-23' ,
                    'US':'2020-03-15' ,
                    'Japan' :'2020-03-16' ,
                    'New Zealand' :'2020-03-23' ,
                    'United Kingdom': '2020-03-24',     
    }
    # source :
    # https://en.wikipedia.org/wiki
    #           /National_responses_to_the_2019%E2%80%9320_coronavirus_pandemic

    # training related
    n_observations = n_days * n_countries
    splits = np.array(np.array_split(np.arange(n_observations), n_countries))

    # discrete labels
    percentiles = [75]
    n_levels = len(percentiles) + 1
    label_dict_two_cat = {0: 'low', 1: 'high'}

    numerical_columns = ['infected', 'infected_new', 'infected_perc_change',
                         'deaths', 'deaths_new', 'deaths_perc_change',
                         'reddit_activity']

    stat_numerical_columns = [
                              'over_65',
                              'reddit_usage',
                              'single_household'
                             ]

    tabu_child_nodes = stat_numerical_columns + ['restriction']
    tabu_parent_nodes = ['reddit_activity', 'sentiment']
    tabu_edges = [
                     ('reddit_usage', 'infected'),
                     ('reddit_usage', 'infected_new'),
                     ('reddit_usage', 'infected_perc_change'),
                     ('reddit_usage', 'deaths'),
                     ('reddit_usage', 'deaths_new'),
                     ('reddit_usage', 'deaths_perc_change'),

                     ('restriction', 'infected'),
                     ('restriction', 'infected_new'),
                     ('restriction', 'infected_perc_change'),
                     ('restriction', 'deaths'),
                     ('restriction', 'deaths_new'),
                     ('restriction', 'deaths_perc_change'),

                     ('over_65', 'reddit_activity'),
                     ('over_65', 'sentiment'),
                     ('single_household', 'reddit_activity'),
                     ('single_household', 'sentiment'),
                     ('reddit_usage', 'sentiment'),
                    ]

    edge_threshold = 0.3


config = Config()
