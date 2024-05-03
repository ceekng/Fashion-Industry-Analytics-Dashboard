from pathlib import Path

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

FILE_PATH = './final_dataset.csv'



@st.cache_data
def read_data(csv_file: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_file)
    return df
df = read_data(FILE_PATH)
price_cols = [col for col in df.columns if '$ stock' in col]
trend_cols = [col for col in df.columns if 'google_trend' in col]
rank_cols = [col for col in df.columns if 'rank' in col]
df[trend_cols] = df[trend_cols].astype(str)


df[trend_cols] = df[trend_cols].apply(lambda x: x.str.replace('<1', '0'))  # Replace '<1' with '0'
df[trend_cols] = df[trend_cols].apply(lambda x: pd.to_numeric(x, errors='coerce'))  # Convert to numeric

# Convert stock price columns to numeric, replacing invalid values with NaN
df[price_cols] = df[price_cols].apply(lambda x: pd.to_numeric(x, errors='coerce'))

# Convert rank columns to numeric, replacing invalid values with NaN
df[rank_cols] = df[rank_cols].apply(lambda x: pd.to_numeric(x, errors='coerce'))


with st.sidebar:
    st.markdown('Use Interactive Data page:')
    companies = st.multiselect(
        'Choose a company',
        options=df['company'].unique(), 
        # max_selections=1,
        default=None
        )
    if companies:
        
        brands = st.multiselect(
            'Choose brand(s)',
            options=df[df['company'].isin(companies)]['brand'].unique(),
            default=None
        )
        if brands:
            data_types = st.multiselect(
                'Trend or Rank',
                options = ["Trend", "Rank"],
                default= None,
                max_selections=1
            )
        else:
            data_types = None
    else:
        brands = None

main_tab, questions, data_source, data_interactive = st.tabs(['Main page', 'Research Questions','Data Sources', 'Interactive Data'])

with data_interactive:
    q_rank_cols = [col for col in df.columns if 'rank' in col]
    q_trend_cols = [col for col in df.columns if 'trend' in col]
    q_stock_cols = [col for col in df.columns if 'stock' in col]
    if (not companies):
        st.info('Please select an company and a brand on the sidebar to the left for the interactive view')
    elif companies and (not brands):
        company_df =df[df['company'].isin(companies)]
        q_stock_cols.insert(0,'company')
        
        stock_df =company_df[q_stock_cols].drop_duplicates()
        stock_df = stock_df.set_index('company')
        
        st.line_chart(stock_df.T) 
    else:
        company_df =df[df['company'].isin(companies)]
        
        temp_df = company_df
        if brands:
            brand_df =df[df['brand'].isin(brands)] 
            temp_df = brand_df
            if data_types:
                if 'Rank' in data_types and 'Trend' in data_types:
                    merged = q_trend_cols + q_rank_cols 
                    merged.insert(0,'company')
                    merged.insert(1,'brand')
                    temp_df = brand_df[merged]
                elif 'Rank' in data_types and 'Trend' not in data_types:
                    q_rank_cols.insert(0,'brand')  
                    temp_df = brand_df[q_rank_cols]
                    temp_df = temp_df.set_index('brand')

                    st.scatter_chart(temp_df.T)
                elif 'Trend' in data_types and 'Rank' not in data_types: 
                    q_trend_cols.insert(0,'brand')
                    temp_df = brand_df[q_trend_cols]
                    temp_df = temp_df.set_index('brand')
                    st.line_chart(temp_df.T)
                    
                else:
                    temp_df = brand_df


with main_tab:
    st.title("DSCI 510 Final Project")
    st.subheader("Exploring the top 3 fashion corporations of interest: LVMH, KERING, and Prada Group and its subsidiary fashion brands")
    st.markdown("By Cheryl Khau")
    st.markdown('''The code for this WebApp reads data from a CSV file, processes it to convert relevant columns to numeric types, and removes unwanted characters (like <1 in Google Trends data).
                The data spans from January 2019 to December 2023, providing a comprehensive timeline to analyze trends, seasonality, and potential long-term shifts.
                ''')
    st.markdown('''
                **Streamlit Tabs:**
                
                1. Main Tab displays introductory information, including explanations of interactivity and data visualization.
                2. Research Question has space for answering project-related questions.
                3. Data Sources provides information on the data sources used in the project.
                4.Interactive contains interactive elements for selecting companies, brands, and data types, with visualizations like line charts and scatter plots.
                
                **Streamlit Sidebar Interaction:**
                
                The sidebar provides options for selecting companies, brands, and data types (Trend or Rank) to influence the interactive view in Interactive Data page.
                
                ''')
    st.markdown('''
                **Gotcha:**
                
                *Data Cleaning and Transformation:*
                Challenge: Data inconsistencies, unexpected null values, or incorrect data types. The stock price data order was reversed at the stage of scraping from API
                Solution: Thoroughly clean and preprocess data, checking for missing values, type mismatches, unexpected characters (like <1), and write mitigation codes.
                
                *Data Mismatches:*
                Challenge: Mismatch between different data sources or incorrect alignment.
                Solution: Validate data consistency, ensuring proper joins and merges.
                
                *Widget Conflicts:*
                Challenge: Multiple data types with the same key (quarter of the years).
                Solution: Ensure unique widget keys and proper scope for interactive elements.

                *Heavy Plots:*
                Challenge: Overloaded plots with excessive data points and types for visualizations.
                Solution: Simplify plots, use appropriate chart types, and consider interactive filtering to reduce data volume to quarterly.   
                
                *Statistical Analysis:*
                Challenge: Lacking coding skills on my end has presented hardship in the ability to fully analyzing the data as expected from the project goal
                Solution: Currently using visual analyzation to identify any possible trend, seasonality, outliers from graphs
                ''')


    # if (not companies):
    #     st.info('Please select an company and a brand on the sidebar to the left for the interactive view')
    # elif companies and (not brands):
    #     company_df =df[df['company'].isin(companies)]
    #     q_stock_cols.insert(0,'company')
        
    #     stock_df =company_df[q_stock_cols].drop_duplicates()
    #     stock_df = stock_df.set_index('company')
        
    #     st.line_chart(stock_df.T) 
    # else:
    #     company_df =df[df['company'].isin(companies)]
        
    #     temp_df = company_df
    #     if brands:
    #         brand_df =df[df['brand'].isin(brands)] 
    #         temp_df = brand_df
    #         if data_types:
    #             if 'Rank' in data_types and 'Trend' in data_types:
    #                 merged = q_trend_cols + q_rank_cols 
    #                 merged.insert(0,'company')
    #                 merged.insert(1,'brand')
    #                 temp_df = brand_df[merged]
    #             elif 'Rank' in data_types and 'Trend' not in data_types:
    #                 q_rank_cols.insert(0,'brand')  
    #                 temp_df = brand_df[q_rank_cols]
    #                 temp_df = temp_df.set_index('brand')

    #                 st.scatter_chart(temp_df.T)
    #             elif 'Trend' in data_types and 'Rank' not in data_types: 
    #                 q_trend_cols.insert(0,'brand')
    #                 temp_df = brand_df[q_trend_cols]
    #                 temp_df = temp_df.set_index('brand')
    #                 st.line_chart(temp_df.T)
                    
    #             else:
    #                 temp_df = brand_df
        
        
    # Convert rank columns to 'Qx-yyyy' format
    renamed_rank_cols = {col: "Q" + col[1] + "-" + "20"+col[2:4] for col in rank_cols}
    df.rename(columns=renamed_rank_cols, inplace=True)


    # Aggregate monthly stock prices into quarterly values by mean
    quarters = [f"Q{(i % 12) // 3 + 1}-{int(i / 12) + 2019}" for i in range(len(price_cols))]

    # Create a DataFrame for quarterly stock prices and sum the values
    stock_prices_quarterly = df[price_cols].T  # Transpose to group by quarter
    stock_prices_quarterly['Quarter'] = quarters
    quarterly_stock = stock_prices_quarterly.groupby('Quarter').mean().T  # Calculate quarterly mean


    q = [col.split('-') for col in quarterly_stock.columns]
    quarters_df = pd.DataFrame(q, columns=['Quarter', 'Year'])

    # Sort by year and quarter
    quarters_df['Year'] = quarters_df['Year'].astype(int)  # Convert year to integer for sorting
    quarters_df_sorted = quarters_df.sort_values(by=['Year', 'Quarter'])

    # Reconstruct sorted column names
    sorted_columns = [f"{row['Quarter']}-{row['Year']}" for index, row in quarters_df_sorted.iterrows()]

    # Reorder DataFrame columns
    quarterly_stock = quarterly_stock.reindex(columns=sorted_columns)
    # Aggregate weekly Google trend data into quarterly values by sum
    trend_quarters = [f"Q{(i % 52) // 13 + 1}-{int(i / 52) + 2019}" for i in range(len(trend_cols))]

    google_trends_quarterly = df[trend_cols].T
    google_trends_quarterly['Quarter'] = trend_quarters
    quarterly_trend = google_trends_quarterly.groupby('Quarter').sum().T



    # Sort by year and quarter
    quarters_df['Year'] = quarters_df['Year'].astype(int)  # Convert year to integer for sorting
    quarters_df_sorted = quarters_df.sort_values(by=['Year', 'Quarter'])

    # Reconstruct sorted column names
    sorted_columns = [f"{row['Quarter']}-{row['Year']}" for index, row in quarters_df_sorted.iterrows()]

    # Reorder DataFrame columns
    quarterly_trend = quarterly_trend.reindex(columns=sorted_columns)
    # Ensure both quarterly datasets have the same length
    assert len(quarterly_stock.columns) == len(quarterly_trend.columns), "Data length mismatch between quarterly stock and trend."

    
    # Get the list of unique companies
    unique_companies = df['company'].unique()


    # Select the columns 'company', 'brand', and ranks
    selected_columns = ["company", "brand"] + list(renamed_rank_cols.values())

    # Create df_quarterly with the required columns
    df_quarterly = df[selected_columns]
    df_quarterly.head()
    # Find all the quarter columns
    quarter_cols = [col for col in df_quarterly.columns if "Q" in col]

    st.subheader('Stock Prices vs Brands Hotness Ranking by Company', divider = 'blue')
    quarterly_stock = quarterly_stock.drop(columns='Q1-2024')
    quarterly_trend = quarterly_trend.drop(columns='Q1-2024')
    # # Merge the DataFrames to align company information
    # combined_df = quarterly_trend.merge(quarterly_stock, on='index', suffixes=('_rank', '_stock'), how='right')

    combined_df = pd.merge(quarterly_stock, quarterly_trend, left_index=True, right_index=True, how='inner', suffixes=('_stock', '_trend'),)
    combined_df = pd.merge(df_quarterly, combined_df, left_index=True, right_index=True, how='inner')


    # Find all the quarter columns for stock prices and brand rankings


    q_stock_cols = [col for col in combined_df.columns if "stock" in col]
    q_rank_cols = [col for col in df_quarterly.columns if 'Q' in col]
    q_trend_cols = [col for col in combined_df.columns if "trend" in col]


    # Create subplots for each company
    fig, axes = plt.subplots(nrows=len(unique_companies), figsize=(12, len(unique_companies) * 6), sharex=True)

    # Plot stock prices and brand ranks for each company
    for i, company in enumerate(unique_companies):
        company_df = combined_df[combined_df['company'] == company]
        company_stock_df = company_df[q_stock_cols]
        company_stock_df = company_stock_df[company_stock_df.columns[::-1]]
        
        # Create a secondary y-axis for stock prices
        ax1 = axes[i]
        ax2 = axes[i].twinx()

        # Plot the stock prices
        ax2.plot(
            q_rank_cols,
            company_stock_df.mean(axis=0),  # Assuming each company has unique stock prices
            color='black',
            linewidth=2,
            label=f"{company} Stock Price"
        )
        # Plot brand rankings on the secondary y-axis
        brands = company_df['brand']
        for brand in brands:
            brand_df = company_df[company_df['brand'] == brand]


            ax1.plot(
                list(q_rank_cols),
                brand_df[q_rank_cols].iloc[0].values,
                linestyle='--',
                label=brand
            )

        # axes[i].invert_yaxis()  # Invert y-axis for brand ranks
        ax1.set_ylabel("Brand Rank (Lower is Better)")
        ax2.set_ylabel("Stock Price")
        ax1.set_title(f"{company} Stock Prices and Brand Rankings")
        
        # Rotate the x-axis labels by 45 degrees
        axes[i].set_xticks(range(len(q_rank_cols)))  # Set x-tick locations
        axes[i].set_xticklabels(q_rank_cols, rotation=45, ha='right')  # Rotate x-axis labels
        
        ax1.set_ylim(20,0)
        
        # Add legends for both axes
        ax1.legend()
        ax2.legend()

    # Set a common x-axis label
    axes[-1].set_xlabel("Quarter")

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Show the plots
    st.pyplot(fig)

    st.markdown('''
                **Stock Price Trends Volatility:**
                Across companies, there's evident volatility in stock prices. This could reflect broader market trends, company-specific events, or macroeconomic factors.
                For instance, Kering's stock prices ranged from a low of 40.44 in October 2023 to a high of 91.71 in June 2021. LVMH shows even greater fluctuation, with prices ranging from around 321 in early 2019 to a peak of over 945 in mid-2023.
                
                **General Growth:**
                Despite fluctuations, there's a general upward trend for most companies, particularly LVMH. This suggests long-term growth, even with periodic downturns.
                Prada shows a similar pattern, with an initial increase from 2019 to 2023, suggesting positive market sentiment or successful company strategies.
                ''')
    st.subheader('Stock Prices vs Brands Google Trend Searches by Company', divider = 'blue')
    
    st.caption('shown in combined bars')
    #--------------------------------------------------------------------------------------------------
    # Create subplots for each company
    fig, axes = plt.subplots(nrows=len(unique_companies), figsize=(12, len(unique_companies) * 6), sharex=True)

    # Plot stock prices and brand ranks for each company
    for i, company in enumerate(unique_companies):
        company_df = combined_df[combined_df['company'] == company]
        
        company_stock_df = company_df[q_stock_cols]
        company_stock_df = company_stock_df[company_stock_df.columns[::-1]]
        
        # Create a secondary y-axis for stock prices
        ax1 = axes[i]
        ax2 = axes[i].twinx()

        # Plot the stock prices
        ax2.plot(
            q_rank_cols,
            company_stock_df.mean(axis=0),  # Assuming each company has unique stock prices
            color='black',
            linewidth=2,
            label=f"{company} Stock Price"
        )
        # Plot brand rankings on the secondary y-axis
        brands = company_df['brand']
        for brand in brands:
            brand_df = company_df[company_df['brand'] == brand]


            ax1.bar(
                list(q_rank_cols),
                brand_df[q_trend_cols].iloc[0].values,
                
                label=brand
            )

        # axes[i].invert_yaxis()  # Invert y-axis for brand ranks
        ax1.set_ylabel("Brand Google Trend Searches")
        ax2.set_ylabel("Stock Price")
        ax1.set_title(f"{company} Stock Prices and Brand Google Trend Searches")
        
        # Rotate the x-axis labels by 45 degrees
        axes[i].set_xticks(range(len(q_rank_cols)))  # Set x-tick locations
        axes[i].set_xticklabels(q_rank_cols, rotation=45, ha='right')  # Rotate x-axis labels
        
        
        
        # Add legends for both axes
        ax1.legend()
        ax2.legend()

    # Set a common x-axis label
    axes[-1].set_xlabel("Quarter")

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Show the plots
    st.pyplot(fig)

    #------------------------------------------------------------------------------------------------------------------------
    st.subheader('Stock Prices vs Brands Google Trend Searches by Company', divider = 'blue')
    
    st.caption('shown in separated bars')
    # Create subplots for each company
    fig, axes = plt.subplots(nrows=len(unique_companies), figsize=(12, len(unique_companies) * 6), sharex=True)

    # Plot stock prices and brand ranks for each company
    for i, company in enumerate(unique_companies):
        company_df = combined_df[combined_df['company'] == company]
        
        company_stock_df = company_df[q_stock_cols]
        company_stock_df = company_stock_df[company_stock_df.columns[::-1]]
        # Create a secondary y-axis for stock prices
        ax1 = axes[i]
        ax2 = axes[i].twinx()

        # Plot the stock prices
        ax2.plot(
            q_rank_cols,
            company_stock_df.mean(axis=0),  # Assuming each company has unique stock prices
            color='black',
            linewidth=2,
            label=f"{company} Stock Price"
        )
        # Plot brand rankings on the secondary y-axis
        brands = company_df['brand']
        
        x = np.arange(len(q_rank_cols)) 
        width =0.1
        multiplier = 0
        
        for brand in brands:
            brand_df = company_df[company_df['brand'] == brand]

            offset = width *multiplier
            rects = ax1.bar(
                x +offset,
                brand_df[q_trend_cols].iloc[0].values,
                width,
                label=brand
            )
            ax1.bar_label(rects, padding=3)
            multiplier+=1

        # axes[i].invert_yaxis()  # Invert y-axis for brand ranks
        ax1.set_ylabel("Brand Google Trend Search")
        ax2.set_ylabel("Stock Price")
        ax1.set_title(f"{company} Stock Prices and Brand Google Trend Searches")
        
        # Rotate the x-axis labels by 45 degrees
        axes[i].set_xticks(range(len(q_rank_cols)))  # Set x-tick locations
        axes[i].set_xticklabels(q_rank_cols, rotation=45, ha='right')  # Rotate x-axis labels
        
        
        
        # Add legends for both axes
        ax1.legend()
        ax2.legend()

    # Set a common x-axis label
    axes[-1].set_xlabel("Quarter")

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Show the plots
    st.pyplot(fig)
    st.subheader('Brand Search on Google Trend vs Brands Hotness Ranking by Brands', divider = 'blue')
    fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(12,12), sharex=True)
    subdf = combined_df[q_trend_cols + q_rank_cols + ['brand']]
    brands = subdf['brand']

    row = 0 
    col = 0
    for brand in brands:
        ax1 = axes[row][col]
        ax1.set_title(brand)
        ax2 = ax1.twinx()
        sbdf = subdf[subdf['brand'] == brand]
        ax1.plot(q_rank_cols, sbdf[q_trend_cols].iloc[0].values, color='red')
        ax2.invert_yaxis()
        ax2.plot(q_rank_cols, sbdf[q_rank_cols].iloc[0].values)
        col += 1
        if col == 4:
            col=0
            row+=1
    # Rotate the x-axis labels by 45 degrees
        ax1.set_xticks(range(len(q_rank_cols)))  # Set x-tick locations
        ax1.set_xticklabels(q_rank_cols, rotation=45, ha='right')  # Rotate x-axis labels
    # Show the plots
    st.pyplot(fig)
    st.markdown('''
                **Lack of Clear Correlation:**
                The analysis suggests that, in general, there is no consistent correlation between Google Trend searches and The Lyst's Hotness brand ranking index for most fashion brands. This could indicate that online search interest does not always align with the rankings of the hottest brands.
                
                **Notable Patterns**:
                Despite the general trend, I found exceptions with some brands, indicating that certain brands show a closer relationship between their Google Trend search volumes and their Lyst rankings.
                For example, Prada, miu miu (part of the Prada Group), and loewe (from LVMH) demonstrate more similar patterns between their search trends and rankings. This suggests that for these brands, online search interest might be a better indicator of their ranking on the Hotness index.
                ''')
    
    
    st.header('Key Insights:')
    st.markdown('''
                **Stock Price Volatility:**
                The stock prices of fashion corporations like Kering, LVMH, and Prada display significant volatility over time, suggesting these companies are sensitive to market trends and broader economic factors.
                Despite fluctuations, most companies demonstrate an upward trend in their stock prices, indicating long-term growth and resilience.
                
                **Consistency Across Brands:**
                In the brand ranking and Google Trend analysis, many brands do not show clear correlations between hotness rankings and Google search trends. However, a few exceptions (like Prada, Miu Miu, and Loewe) suggest certain brands maintain consistent popularity across different metrics.
                
                **Quarterly Stock Price Peaks and Troughs:**
                There are notable peaks and troughs in stock prices that often align with significant external events. For example, LVMH's stock prices dropped significantly in early 2020 during the COVID-19 pandemic but rebounded thereafter, reflecting resilience.
                
                **Brand Popularity vs. Stock Prices:**
                The correlation between brand popularity (as indicated by hotness rankings) and stock prices is not always clear. However, certain brands might have a more direct impact on the parent company's stock, which could indicate the brand's influence within the corporation.''')
    st.header('Possible Implications:')
    
    st.markdown('''
                **Corporate Strategy:**
                For the parent companies, these trends suggest that diversifying the brand portfolio and maintaining flexibility during market downturns could be key to long-term success.
                Brands that show consistent popularity might warrant further investment in marketing and product development, as they could be driving factors for corporate growth.
                
                **Market Sensitivity:**
                Given the volatility in stock prices, companies in the fashion industry need to be adaptable to external shocks, such as economic downturns or global events like pandemics.
                
                **Correlation with Brand Popularity:**
                Brands that influence stock prices may indicate a significant level of consumer confidence or market share. Understanding this correlation could help companies strategize their marketing and product development efforts to maximize impact.''')
with data_source:
    st.markdown('''
        Exploring the top 3 fashion corporations of interest: LVMH, KERING, and Prada Group and its subsidiary fashion brands
https://fashionretail.blog/2019/04/08/luxury-and-fashion-corporations/ 

The article provides the top powerful corporations in Luxury fashion industry and their subsidiary brands. 

    '''
    )

    st.markdown('''
        DATA SOURCE 1 Top 20 fashion brands’ hotness 
        URL for website to scrape: https://www.lyst.com/data/the-lyst-index/
        The Lyst Index provides a quarterly ranking of fashion's hottest brands and products,, starting Q3 2018. It includes data on top 20 brands popularity and 10 hottest products.

        DATA SOURCE 2: Brands’ stock prices
        API: https://twelvedata.com/
        
        https://twelvedata.com/ offers access to trading data for US stocks. This dataset provides valuable information on brand-related stocks and their market performance.

        DATA SOURCE 3: Manually download selected brands’ interest over time data from Google Trends
        
        Google Trends https://trends.google.com/trends/ 
        Google Trends providies insights into the popularity and search interest of various topics, including fashion brands. This dataset offers data on the relative search volume of fashion brands over time.
    '''
    )

with questions:
    st.markdown('''

        1. What did I set out to study? 
        
        The goal of this project is to visualize and study the influence between stock prices, brand rankings, and Google Trends data for major fashion corporations like LVMH, Kering, and Prada Group, along with their subsidiary brands. It explores whether trends in these datasets can indicate changes in market performance.

        2. What were the findings?
        
        My conclusions are based on the visualizations and data analysis. 
        
        3. What difficulties did I have in completing the project?
        
        Lacking coding skills in order to better statistically exploring the data.
        
        4. What skills did I wish I had while doing the project?
        
        See above
        
        5. What would I do “next” to expand the project?
        
        I would definitely learn to better my coding skills and statistical analyzing ability in order to deduce any key findings based on this data
        
    '''
    )

