---
title: "Deep Learning"
source: "https://learn.udacity.com/nd101?version=15.0.10&partKey=cd1822&lessonKey=bc0eb07b-bd9c-4924-bb9b-59159e72d916&project=rubric"
author:
published:
created: 2026-02-04
description:
tags:
  - "clippings"
---
## Rubric

Use this project rubric to understand and assess the project criteria.

## Fetch data

| Criteria | Submission Requirements |
| --- | --- |
| Create a single dataframe by fetching data from the 3 CSV files. The dataframe should have the following columns -> \["Title", "Year", "Synopsis", "Review", and "Original Language"\]. | Students are able to create a Pandas dataframe of movie reviews by completing the `preprocess_data()` function. |

## Text Translation

| Criteria | Submission Requirements |
| --- | --- |
| Load translation models and tokenizers from HuggingFace | Students are able to load the pretrained text translation models and tokenizers from HuggingFace. |
| Write a function to translate text using a model and a tokenizer (Complete `translate()`) | Students are able to complete the translate() function. |
| Filter French and Spanish reviews and synopses in the dataframe and translate them to English. | Students should be able to use the translate() function to translate French and Spanish reviews and synopses to English and then update the dataframe. |

## Sentiment Analysis

| Criteria | Submission Requirements |
| --- | --- |
| Analyze the sentiment of all the reviews in the dataframe using a pre-trained model from HuggingFace. Report sentiments as Negative/Positive by creating a new column called "Sentiment". | Students should load a sentiment analysis model, complete the function called `analyze_sentiment`, and then get the Sentiment (Negative, Positive) of all the movie reviews in the dataframe. |

