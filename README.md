# Netflix Data Insights Dashboard

## Overview

Netflix Data Insights Dashboard is an interactive Streamlit application designed to explore and analyze Netflix content data through dynamic visualizations and filtering options. The dashboard enables users to discover trends in content types, genres, ratings, directors, countries, and yearly content growth.

## Features

### Interactive Filters

* Filter content by Year Added
* Filter content by Country
* Filter content by Genre
* Real-time dashboard updates

### Dashboard Analytics

#### 1. Content Type Distribution

* Movies vs TV Shows
* Pie Chart Visualization
* Bar Chart Visualization

#### 2. Genre Analysis

* Top 10 Genres
* Genre Distribution Pie Chart

#### 3. Content Growth Analysis

* Titles Added Per Year
* Trend Line Visualization

#### 4. Director Analysis

* Top 10 Directors by Content Count

#### 5. Word Cloud Visualization

* Movie Title Word Cloud

#### 6. Country Analysis

* Top Content Producing Countries
* Country Distribution Charts

#### 7. Ratings Analysis

* Ratings Distribution
* Rating Popularity Comparison

## Technologies Used

* Python
* Streamlit
* Pandas
* Matplotlib
* Seaborn
* WordCloud
* NumPy

## Project Structure

```text
Netflix/
│
├── netflix_dashboard.py
├── netflix_cleaned.csv
├── requirements.txt
├── screenshots/
└── README.md
```

## Installation

### Clone Repository

```bash
git clone https://github.com/grishu21/Netflix-Data-Analysis-Dashboard.git
cd Netflix-Data-Analysis-Dashboard
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Dashboard

```bash
streamlit run netflix_dashboard.py
```

The dashboard will open automatically in your browser at:

```text
http://localhost:8501
```

## Dashboard Highlights

* Netflix-themed user interface
* Interactive sidebar filters
* Multiple visualization types
* Dynamic chart updates
* Data-driven insights
* User-friendly analytics dashboard

## Sample Insights Generated

* Distribution of Movies and TV Shows
* Most Popular Netflix Genres
* Content Growth Trends
* Leading Content Producing Countries
* Top Directors on Netflix
* Most Common Content Ratings

## Future Enhancements

* Recommendation System
* Streamlit Cloud Deployment
* Advanced Search Functionality
* User Authentication
* Downloadable Reports
* AI-powered Content Insights


