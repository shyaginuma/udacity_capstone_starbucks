import pandas as pd
import numpy as np
import pandasql as ps

# create features and clean data from portfolio.json
def process_portfolio(portfolio):
    portfolio["num_channel"] = portfolio.channels.map(lambda x: len(x))

    channels = ['web', 'email', 'mobile', 'social']
    for channel in channels:
        col_name = 'channel_' + channel
        portfolio[col_name] = portfolio.channels.map(lambda x: 1 if channel in x else 0)

    portfolio = portfolio.drop(['channels'], axis=1)

    return portfolio

# create features and clean data from transcript.json
def process_transcript(transcript):

    # split dataframe by each event
    offer_received_transcript = transcript[transcript.event == 'offer received']
    offer_viewed_transcript = transcript[transcript.event == 'offer viewed']
    offer_completed_transcript = transcript[transcript.event == 'offer completed']
    transaction_transcript = transcript[transcript.event == 'transaction']

    # extract offer id and amount from value
    offer_received_transcript['offer_id'] = offer_received_transcript.value.map(lambda x: x['offer id'])
    offer_viewed_transcript['offer_id'] = offer_viewed_transcript.value.map(lambda x: x['offer id'])
    offer_completed_transcript['offer_id'] = offer_completed_transcript.value.map(lambda x: x['offer_id'])
    transaction_transcript['amount'] = transaction_transcript.value.map(lambda x: x['amount'])

    return transaction_transcript, offer_received_transcript, offer_viewed_transcript, offer_completed_transcript

def preprocess(portfolio, transcript):

    # process portfolio, transcript
    portfolio = process_portfolio(portfolio)
    transaction_transcript, offer_received_transcript, offer_viewed_transcript, offer_completed_transcript = process_transcript(transcript)

    # create offer deadline
    offer_received_transcript = offer_received_transcript.merge(
        portfolio[['id', 'duration']], how='left', left_on='offer_id', right_on='id'
        ).drop(['id','value'], axis=1)
    offer_received_transcript["offer_deadline"] = offer_received_transcript["time"] + 24 * offer_received_transcript["duration"]

    # add offer id to transactions which related with offer
    transaction_transcript = transaction_transcript.drop('value', axis=1)
    query1 = '''
        SELECT
            L.person,
            L.time,
            L.amount,
            R.time AS offer_received_at,
            R.offer_id,
            R.offer_deadline
        FROM
            transaction_transcript AS L
        LEFT JOIN
            offer_received_transcript AS R
        ON L.person = R.person
        AND L.time BETWEEN R.time AND R.offer_deadline
    '''
    transaction_transcript = ps.sqldf(query1, locals())

    # add when the offer viewed
    offer_viewed_transcript = offer_viewed_transcript[['person', 'time', 'offer_id']]
    offer_viewed_transcript = offer_viewed_transcript.rename(columns={'time': 'offer_viewed_at'})
    transaction_transcript = transaction_transcript.merge(offer_viewed_transcript, how='left', on=['person', 'offer_id'])

    # create the flag which show the transactions were influenced by the offer
    query2 = '''
        SELECT
            *,
            CASE
                WHEN offer_id IS NULL THEN 0
                WHEN offer_viewed_at IS NULL THEN 0
                WHEN time < offer_viewed_at THEN 0
                ELSE 1
            END AS is_influenced_by_offer
        FROM
            transaction_transcript
    '''
    transaction_transcript = ps.sqldf(query2, locals())

    return transaction_transcript