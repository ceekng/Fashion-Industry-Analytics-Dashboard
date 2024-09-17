# Fashion Industry Trends Analysis

An interactive Streamlit dashboard exploring relationships between stock prices, brand rankings, and Google Trends data for major fashion corporations and their subsidiary brands.

## Project Overview

This project aims to analyze the correlations between fashion brand popularity, stock market performance, and consumer interest. By combining data from The Lyst Index, Twelve Data API, and Google Trends, the analysis seeks to uncover patterns that highlight the relationship between brand rankings, stock price fluctuations, and online search interest for key fashion brands under corporations like LVMH, Kering, and Prada Group.

## Technologies Used

Python 3.x
Pandas 2.0.3: Data manipulation and analysis
Matplotlib 3.7.2: Data visualization
Seaborn 0.12.2: Statistical data visualization
Streamlit 1.34.0: Interactive web applications

## Data Sources

1. The Lyst Index: Quarterly ranking of fashion's hottest brands, starting from Q3 2018.
2. Twelve Data API: Stock price data for US-listed fashion brands and corporations.
3. Google Trends: Provides data on search interest and popularity for fashion brands over time.
For more details, refer to [data_sources.md].

## Key Findings

1. Stock Price Volatility:
Across companies like Kering and LVMH, stock prices show evident volatility. For example, Kering’s stock ranged from a low of 40.44 in October 2023 to a high of 91.71 in June 2021, while LVMH’s prices fluctuated from 321 in early 2019 to a peak over 945 in mid-2023.
2. General Growth:
Despite fluctuations, most companies demonstrate an upward trend, indicating long-term growth. LVMH and Prada both show patterns of increasing market performance from 2019 to 2023.
3. Brand Popularity vs Stock Prices:
No consistent correlation exists between brand Google Trends searches and The Lyst Index rankings. However, brands like Prada, Miu Miu, and Loewe show more aligned trends, suggesting that for these brands, search interest may be a more reliable indicator of brand ranking.
4. Quarterly Stock Price Peaks:
LVMH experienced significant price drops during early 2020 due to the COVID-19 pandemic but quickly rebounded, showcasing the company's resilience.

## Setup and Installation

1. Clone this repository
git clone <repository-url>
2. Install the required dependencies:
pip install -r requirements.txt
4. Run the Streamlit app locally
streamlit run app.py


## Project Structure

1. api.py: Fetches stock prices from the Twelve Data API.
2. scraper_brands_rank.py: Scrapes brand rankings from The Lyst Index.
3. model.py: Merges and analyzes stock, trend, and ranking data.

final_dataset.csv: Merged dataset of stock prices, brand rankings, and Google Trends data.

## Streamlit App

https://dsci--510-final-fqdpwduj7njbysosxathkr.streamlit.app/

## Key Visualizations
- Stock Prices vs Brand Google Trend Searches by Company: Displays trends in stock prices and search interest, highlighting potential correlations for brands like Prada, Miu Miu, and Loewe.
- Brand Search vs Hotness Ranking: Showcases the lack of consistent correlation between online search trends and brand rankings, with notable exceptions for certain brands.

## Challenges and Future Work

Challenges:
Handling data integration across different sources (stock prices, rankings, and search interest) posed challenges, particularly with aligning different timeframes.
The analysis revealed that coding proficiency, particularly in advanced statistical methods, would be beneficial to expand the depth of insights.

Future Work:
Enhance the analysis with more sophisticated statistical models to identify and quantify relationships between datasets.
Explore additional data sources, such as social media metrics, to enrich the analysis of brand performance and market trends.
