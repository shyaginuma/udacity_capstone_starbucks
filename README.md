# udacity_capstone_starbucks

This is capstone project of Udacity Data Scientist Nanodegree.  
In many choices, I selected Starbucks project. Because I want to get the experience of facing real company problem with analytics and I like coffee.  
In Starbucks project, we require to analyze related with app offer optimization, such as informational, discount.  
We are provided three data.

- transcript: This is the event log data. This contains events such as offer viewed, bought product, offer received.
- profile: This data contains customer's demographic information.
- portfolio: This data contains offer information.

## ToC

- [Project Motivation](#motivation)
- [Summary](#summary)
- [Installation](#installation)
- [Project Organization](#constraction)

## Project Motivation <a name="motivation"></a>

The offer is one of the most important object of analysis.  
Offer can pulls back users who were sleeping, raises the user's purchase, enhance user engagement, and so on.  
There are several ways of analysis, which is " Who will complete offer? ", " When should we send offer? ", ...etc.  
Here, I will analyze the thema **" How to maxmize the profit from offer? "**.
If we can solve this question, we can know who and what coupons should be sent.

## Summary <a name="summary"></a>

I solve my question by predicting sales of person who received offer with machine learning model.  
First, I preprocess the data to be able to input machine learning model, and create some features.
Then, I build ML models for each offer type (informational, discount, buy one go one free) and evaluate these model, and try some method to improve the models.  
Finally, I predict sales if we sent each person to appropriate offer, and compare with raw data to verify the effect.


## Installation <a name="installation"></a>

### Requirements

- Python3.7

This project managed by [pipenv](https://github.com/pypa/pipenv). So, if you don't install pipenv, please install.

```{}
brew install pipenv
```

When finished install and clone this repositry, run below command.

```{}
pipenv sync
```

When you want to run notebooks, run below command.

```{}
pipenv shell
jupyter notebook
```

## Project Organization <a name="constraction"></a>

```{}
├── Pipfile
├── Pipfile.lock
├── docs
├── notebooks
└── py
```

### Pipfile, Pipfile.lock

These file capture libraries used in notebooks

### docs

The file in this repositry are Udacity provided description.

### notebooks

draft and publish notebooks

### py

functions that transform data used in the notebook