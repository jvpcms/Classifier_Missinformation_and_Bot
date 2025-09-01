# Disinformation and Social Bot Detection in Portuguese

This project, developed under the Institutional Program for Scholarships in Technological Development and Innovation (PIBITI) at the Military Institute of Engineering (IME), focuses on building a dataset to combat disinformation and the activity of social bots in the Portuguese language.

The main objective is to address the scarcity of datasets that integrate labeled news (true or false) with the profiles of users who share them on social networks, classifying them as bots or non-bots.

## Project Overview

The core of the project is an automated process that performs the following steps:
1.  **News Collection**: Extracts and labels news from journalistic sources and reliable fact-checking agencies.
2.  **Social Network Association**: Searches for posts sharing this news on the Bluesky social network.
3.  **User Data Collection**: Stores metadata from the profiles that made the posts.
4.  **Account Classification**: Uses a committee of Machine Learning models to classify accounts as "Social Bot" or "Non-Social Bot".

The result is a structured dataset that allows for the analysis of content dissemination and the training of new detection models.

## Technologies and Concepts Used

* **Database**: MongoDB, chosen for its flexibility in storing semi-structured data.
* **Containerization**: Docker, to ensure the project's environmental reproducibility.
* **Data Collection**: Web scraping of news portals and fact-checking agencies, and consumption of the Bluesky social network API.
* **Machine Learning**: User account classification using a committee of pre-trained models, including:
    * K-Nearest Neighbors
    * Decision Tree
    * Random Forest
    * Logistic Regression
    * Neural Network
* **Natural Language Processing**: Query generation from tokens extracted from news content for social network searching.

## Methodology

The workflow was structured to sequentially collect, process, and classify data, culminating in the creation of the `FakeNewsAndSocialBotSet` dataset.

<img width="1088" height="608" alt="Screenshot from 2025-08-29 02-53-32" src="https://github.com/user-attachments/assets/a1c3a61e-683e-4dec-a702-ffd08432b76e" />

1.  **Identify Labeled News**: News is collected from sources like G1, Aos Fatos, and e-Farsas, among others, and labeled as true or false. News from journalistic outlets is considered true by default.
2.  **Associate and Collect Posts**: Search queries are generated from the news text and submitted to the Bluesky API to find related posts.
3.  **Collect Account Data**: For each post found, the author's profile data is extracted and stored.
4.  **Account Classification**: Profiles are classified as *bot* or *non-bot* based on a strict consensus criterion on the classification results of the different models.
