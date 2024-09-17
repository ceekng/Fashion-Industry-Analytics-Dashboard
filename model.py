import pandas as pd

KERING_BRANDS = ["balenciaga", "gucci", "bottega veneta", "saint laurent"]
LVMH_BRANDS = ["louis vuitton", "dior", "fendi", "jw anderson", "loewe", "off-white"]
PRADA_BRANDS = ["prada", "miu miu"]


def read_brands_data():
    data = {"company": [], "brand": []}

    for brand in KERING_BRANDS:
        data["company"].append("Kering")
        data["brand"].append(brand)

    for brand in LVMH_BRANDS:
        data["company"].append("LVMH")
        data["brand"].append(brand)

    for brand in PRADA_BRANDS:
        data["company"].append("Prada")
        data["brand"].append(brand)

    df = pd.DataFrame(data)
    return df


def parent_child_rank_df_compose(brand_df, parent_df):
    # get quarter code
    brand_df["qstr"] = brand_df["Quarter"].astype(int).astype(str)
    brand_df["ystr"] = (brand_df["Year"] % 100).astype(int).astype(str)
    brand_df["code"] = "q" + brand_df["qstr"] + brand_df["ystr"] + " (rank)"

    brand_df = brand_df.drop("Quarter", axis="columns")
    brand_df = brand_df.drop("Year", axis="columns")
    brand_df = brand_df.drop("qstr", axis="columns")
    brand_df = brand_df.drop("ystr", axis="columns")

    brand_df.set_index("code", inplace=True)
    brand_df = brand_df.transpose()

    brand_df["brand"] = brand_df.index
    brand_df = pd.merge(brand_df, parent_df, on="brand")

    cols_to_move = ["company", "brand"]
    brand_df = brand_df[
        cols_to_move + [x for x in brand_df.columns if x not in cols_to_move]
    ]

    return brand_df


def clean_data_for_stock(stock_df):
    stock_df = stock_df.drop("Unnamed: 0", axis="columns")

    stock_df["time"] = stock_df["time"].astype("string")
    stock_df["time"] = stock_df["time"] + " ($ stock)"
    stock_df = stock_df.set_index("time")
    stock_df = stock_df.transpose()
    stock_df["company"] = stock_df.index

    cols_to_move = ["company"]
    stock_df = stock_df[
        cols_to_move + [x for x in stock_df.columns if x not in cols_to_move]
    ]
    return stock_df


def get_google_trend_df():
    # Google trend CSV files were manually download from Googletrend website. Max 5 variables
    # Read the CSV files into pandas DataFrames, excluding the first two lines
    df1 = pd.read_csv("./google-trends/Googletrend_Kering_brands.csv", skiprows=2)
    df2 = pd.read_csv("./google-trends/Googletrend_LVMH_brands1.csv", skiprows=2)
    df3 = pd.read_csv("./google-trends/Googletrend_LVMH_brands2.csv", skiprows=2)
    df4 = pd.read_csv("./google-trends/Googletrend_Prada_Group_brands.csv", skiprows=2)

    # Check for the same date range
    if (
        (df1["Week"] == df2["Week"]).all()
        and (df2["Week"] == df3["Week"]).all()
        and (df3["Week"] == df4["Week"]).all()
    ):
        # Merge the DataFrames based on the common date column
        merged_GoogleTrend_df = pd.merge(df1, df2, on="Week")
        merged_GoogleTrend_df = pd.merge(merged_GoogleTrend_df, df3, on="Week")
        merged_GoogleTrend_df = pd.merge(merged_GoogleTrend_df, df4, on="Week")
    else:
        print("DataFrames do not have the same date range.")

    merged_GoogleTrend_df = merged_GoogleTrend_df.set_index("Week")

    def converter(x):
        return x.lower()[0:-17]

    merged_GoogleTrend_df = merged_GoogleTrend_df.rename(columns=converter)
    merged_GoogleTrend_df = merged_GoogleTrend_df.rename(
        columns={"yves saint laurent": "saint laurent"}
    )

    # unmatch rows for merging
    merged_GoogleTrend_df = merged_GoogleTrend_df.drop("lvmh", axis="columns")
    merged_GoogleTrend_df = merged_GoogleTrend_df.drop("prada group", axis="columns")
    merged_GoogleTrend_df = merged_GoogleTrend_df.drop("kering brands", axis="columns")

    merged_GoogleTrend_df = merged_GoogleTrend_df.transpose()

    def add_detail_columns(x):
        return str(x) + "( google_trend weekly)"

    merged_GoogleTrend_df = merged_GoogleTrend_df.rename(columns=add_detail_columns)

    merged_GoogleTrend_df["brand"] = merged_GoogleTrend_df.index

    cols_to_move = ["brand"]
    merged_GoogleTrend_df = merged_GoogleTrend_df[
        cols_to_move
        + [x for x in merged_GoogleTrend_df.columns if x not in cols_to_move]
    ]

    return merged_GoogleTrend_df


def main():
    parent_df = read_brands_data()
    stock_df = pd.read_csv("./brands_stock.csv")
    brand_df = pd.read_csv("./brands_rank.csv")

    # Adjust data consistency in rank
    for x in brand_df.columns:
        brand_df[x] = brand_df[x].astype("Int64")

    brand_df = parent_child_rank_df_compose(brand_df=brand_df, parent_df=parent_df)
    stock_df = clean_data_for_stock(stock_df=stock_df)
    merge_df = pd.merge(brand_df, stock_df, on="company")

    google_trend_df  = get_google_trend_df()
    merge_df = pd.merge(merge_df, google_trend_df, on="brand")

    merge_df.to_csv("./final_dataset.csv")


main()
