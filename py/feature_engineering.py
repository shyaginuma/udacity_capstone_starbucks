import pandas as pd
import numpy as np

def create_feature(transaction, portfolio, profile):

    # split data to offer related and not related
    offer_related_transaction = transaction[transaction.is_influenced_by_offer == 1]
    offer_not_related_transaction = transaction[transaction.is_influenced_by_offer == 0]

    # created target valuable
    offer_related_transaction = offer_related_transaction.groupby(['person', 'offer_id'])['amount'].sum().reset_index()

    # merge other data and add features
    offer_related_transaction = offer_related_transaction.merge(profile, how='left', left_on='person', right_on='id').drop('id', axis=1)
    offer_related_transaction = offer_related_transaction.merge(portfolio, how='left', left_on='offer_id', right_on='id').drop('id', axis=1)

    # create feature from offer not related transactions
    offer_not_related_transaction = offer_not_related_transaction[['person', 'amount']]
    aggfunc = {
        'amount': ['min', 'max', 'sum', 'mean', 'count', 'std', 'median']
    }
    offer_not_related_transaction = offer_not_related_transaction.groupby('person')['amount'].agg(aggfunc).reset_index()
    offer_not_related_transaction.columns = ['_'.join(col) for col in offer_not_related_transaction.columns]
    offer_related_transaction = offer_related_transaction.merge(offer_not_related_transaction, how='left', left_on='person', right_on='person_').drop('person_', axis=1)
    offer_related_transaction = offer_related_transaction.fillna(0)

    # drop income, gender, age is null users
    offer_related_transaction = offer_related_transaction[offer_related_transaction.age != 118]

    # create other feature
    offer_related_transaction['became_member_on'] = pd.to_datetime(offer_related_transaction.became_member_on.map(lambda x: str(x)), format='%Y%m%d')
    offer_related_transaction['registar_year'] = offer_related_transaction['became_member_on'].dt.year
    offer_related_transaction['registar_month'] = offer_related_transaction['became_member_on'].dt.month
    offer_related_transaction['scaled_difficulty'] = offer_related_transaction.difficulty / offer_related_transaction.duration
    offer_related_transaction['age_group'] = np.floor(offer_related_transaction.age/10) *10
    offer_related_transaction['buy_rate'] = offer_related_transaction.amount_sum / offer_related_transaction.income
    offer_related_transaction['reward_inpact'] = offer_related_transaction.reward / offer_related_transaction.income
    offer_related_transaction['income_growth_potential'] = offer_related_transaction.income / offer_related_transaction.age

    # get dummy valuables
    offer_related_transaction = pd.get_dummies(offer_related_transaction, columns=['gender', 'registar_year'])

    # log scaling target valuable
    offer_related_transaction['amount_log'] = np.log(offer_related_transaction.amount)

    # drop not needed columns
    offer_related_transaction = offer_related_transaction.drop([
        'became_member_on',
        'channels'], axis=1
    )

    return offer_related_transaction