---
title: "Data Analyst"
source: "https://learn.udacity.com/nd002?version=13.0.23&partKey=cd12531&lessonKey=ls14991&project=rubric"
author:
published:
created: 2026-02-04
description:
tags:
  - "clippings"
---
## Rubric

Use this project rubric to understand and assess the project criteria.

## Code Quality and Submission Phase

| Criteria | Submission Requirements |
| --- | --- |
| Does the code work? | All code is functional (i.e. no errors are thrown by the code). Warnings are okay, as long as they are not a result of poor coding practices. |
| The student has uploaded a.zip folder containing their Jupyter Notebook for code review, and their datasets (file/link) for running the code. | The `.zip` folder contains the following:  - A Jupyter Notebook with all code completed and executed without errors. - The datasets used, or a `.txt` file with links to the datasets if they were downloaded manually. - The code used to gather data if it was done programmatically (e.g., API code or web scraping) should be in the notebook. - The raw datasets saved locally before cleaning. - The final cleaned dataset saved locally after combining datasets and removing unnecessary variables. |
| The project shows thorough documentation of justification of wrangling decisions. | \| The student should ensure the project is well-documented. For each part, they should explain why they chose specific methods for gathering, assessing, cleaning, and storing data and answering the research question.   1) Comments are added to the code to make it easy to understand. 2) All required parts marked `FILL IN` are replaced with relevant contents. 3) At least **two visuals** should be included in the **Answering the Research Question** section, and **each visual should be explained** in terms of how it helps address the research question. \| |

## Gathering, Assessment, and Cleaning

| Criteria | Submission Requirements |
| --- | --- |
| The project has a proper explanation of the problem statement. | Students write 2-4 full sentences explaining the kind of problem they will want to look at and the datasets they will be wrangling for this project. |
| The student has gathered at least two separate datasets using two different data gathering methods. | Students should pick at least two data sources, which may come from the same or different gathering methods listed below:  - Download data manually - Programmatically downloading files - Gather data by accessing APIs - Gather and extract data from HTML files using BeautifulSoup - Extract data from a SQL database  Students must then gather at least two datasets. Each dataset must have **at least two variables and have greater than 500 data samples within each dataset**.  For each dataset, students must describe in 2-3 full sentences:  - Why they picked the dataset - The gathering method - The names and significance of the variables in the dataset.  For applicable data gathering methods, such as parsing HTML, extracting SQL data, and programmatic API access, students must show their work (e.g., if using an API to download the data, please include a snippet of your code in the notebook). |
| The student assesses the datasets for quality and tidiness. | Students should list **two** data quality issues and **two** data tidiness issues with the datasets they have selected. For each data issue, they should:  - Briefly describe the issue they find. - Assess the issue visually (e.g., `df.head()`) **and** programmatically (e.g., `df.describe()`) using the methods discussed in the course. - Justify the assessment methods.  **Hint:** When assessing data, use the following guidelines:\*\*\*\*  - **Data Quality Pillars:** Completeness, Validity, Accuracy, Consistency, Uniqueness. - **Data Tidiness Rules:** Each variable forms a column, each observation forms a row, each type of observational unit forms a table.  Avoid including feature engineering or dimensionality reduction as “issues.” Focus on real data quality and tidiness problems. |
| The student cleans the data issues they identified with the explanation and justifications. | Students should clean the dataset to solve the 4 issues corresponding to data quality and tidiness in the assessment step. For each issue cleaned, they must:  - Include justifications for the cleaning method used and cleaning decisions. - Use **either** the visual or programmatical method to validate that the cleaning was successful |
| Remove unnecessary variables and combine datasets | Students must remove unnecessary variables for their analysis and combine their datasets. After combining the data, the final dataset must have **at least** 4 variables. |

## Data Storage and Answering the Research Question

| Criteria | Submission Requirements |
| --- | --- |
| Students must update their data store. | Update your database/data store with the cleaned data  - Students must maintain different instances/versions of data (raw data and cleaned data) - Students must use clear, descriptive file names (e.g., `raw_data.csv`, `cleaned_data.csv`) - Students must ensure both the raw and cleaned data are saved to their database/data store  Note: Students are not required to use a relational/non-relational database store. |
| Students will define and answer a short research question. | Students must use the final cleaned data to answer the question they raised from the problem statement in Step 1.  - Students must **produce at least two visualizations** using the cleaned data - **Each visual is accompanied by explanations** that describe how the question is answered in 1-2 sentences. - The answer should be clear and supported by the visuals. |
| Students must identify next steps for the project. | In 2-4 sentences, students must describe what actions they would take if they had more time to complete the project.  **Hint:** Discuss any data quality or tidiness issues you would explore further and any other research questions you would consider. |

