from crawlers.fbref.cleaning import clean_df


def parse_soccerdata_table(df, table_name: str):
    return clean_df(df, table_name)