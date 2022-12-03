'''
utility functions related to data
'''

import numpy as np
import pandas as pd

import reverse_geocoder as rg

from configs import config as cf


def reformat_date(date_to_be_formatted):
    '''transform column to YYYY-MM-DD'''

    date_split = date_to_be_formatted.split('/')
    date_padded_split = [str(item).zfill(2) for item in date_split]
    date_formatted = '20{}-{}-{}'.format(date_padded_split[2],
                                         date_padded_split[0],
                                         date_padded_split[1])

    return(date_formatted)


def reformat_dataframe(dataframe_to_be_formatted):
    '''
    Groupby (sum) Country & drop 'Province/State', 'Lat', 'Long'
    '''

    # shorten colum name
    dataframe_to_be_formatted = dataframe_to_be_formatted.rename(
        columns={'Country/Region': 'Country'},  inplace=False
    )

    # drop some columns
    dataframe_to_be_formatted = dataframe_to_be_formatted.drop(
        columns=['Province/State', 'Lat', 'Long'], axis=0, inplace=False
    )
    dataframe_formatted = dataframe_to_be_formatted.groupby(['Country']).sum()

    # change column name format
    for column in dataframe_formatted:
        dataframe_formatted = dataframe_formatted.rename(
            columns={column: reformat_date(column)}
        )

    # rolling window of 2
    dataframe_formatted = dataframe_formatted.rolling(
                                                      window=3,
                                                      win_type=None,
                                                      axis=1
                                                      ).mean().round(
                                                      ).fillna(
                                                      value=0
                                                      ).astype(int)

    # filter with dates
    dataframe_formatted = dataframe_formatted.iloc[
                            :, dataframe_formatted.columns <= cf.end_date]
    dataframe_formatted = dataframe_formatted.iloc[
                            :, dataframe_formatted.columns >= cf.start_date]

    return(dataframe_formatted)


def read_covid(data_path, columns='all'):
    '''
    read official covid data
    '''
    if columns == 'all':
        covid = pd.read_csv(data_path)
    else:
        covid = pd.read_csv(data_path, usecols=columns)
    # remove incorrect entry of lat and long zeros
    covid = covid[~np.logical_and(covid.Long == 0, covid.Long == 0)]

    return covid


def read_reddit_data(data_path):
    '''
    read posts data
    '''

    posts = pd.read_csv(data_path)
    posts.drop_duplicates(inplace=True, subset='id')

    return posts


def add_missing_countries(posts_df):
    '''
    Note: this functions work 'inplace'
    '''

    print('{} posts do not have country information!'.format(
                                        posts_df['Location'].isna().sum()))

    # get posts without a country info
    no_country = posts_df[posts_df['Location'].isna()][
                                            ['Lat', 'Long']].drop_duplicates()

    # extract coordinates
    coordinates = list(no_country.itertuples(index=False, name=None))

    # map coordinates with countries using an external package
    results = rg.search(coordinates)
    no_country['found_countries'] = [i['cc'] for i in results]
    no_country['found_countries'] = no_country[
                        'found_countries'].map(cf.country_abbr)
    no_country['Lat_Long'] = no_country[['Lat', 'Long']].apply(
                                        lambda x: '_'.join(x.map(str)), axis=1)

    # add mapped countries to the original posts data
    posts_df.loc[posts_df['Location'].isna(), 'Location'] = list(posts_df[
                            posts_df['Location'].isna()]['Lat_Long'
                                                          ].map(
                    dict(zip(
                          no_country['Lat_Long'], no_country['found_countries']
                                                    ))))
    posts_df.drop(['Lat_Long'], axis=1, inplace=True)

    print('{} posts that do not have country information will be discarded!'
          .format(posts_df['Location'].isna().sum()))
    posts_df = posts_df[~posts_df['Location'].isna()]

    return None
