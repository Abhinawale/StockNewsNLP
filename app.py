import pandas as pd
import requests
import spacy
from bs4 import BeautifulSoup
import streamlit as st
import yfinance as yf
import lxml

st.title("Treading Stocks In News:zap:")

nlp = spacy.load("en_core_web_sm")


def extract_text_from_rss(rss_link):
    headings = []
    
    r1 = requests.get("https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms")
    r2 = requests.get(rss_link)
    soup1 = BeautifulSoup(r1.content, features='html.parser')
    soup2 = BeautifulSoup(r2.content, features='html.parser')
    headings1 = soup1.findAll('title')
    headings2 = soup2.findAll('title')
    headings= headings1+headings2
    return headings


def generate_stock_info(headings):
    

    stock_info_dict = {


        'Org': [],
        'Symbol': [],
        'currentPrice':[],
        'dayHigh' : [],
        'dayLow' : [],
        #'forwardPE' : [],
        #'divedendYield' : []
    }

    stocks_df = pd.read_csv("./data/ind_nifty500list.csv")
    for title in headings:
        doc = nlp(title.text)
        for ent in doc.ents:
            try:
                if stocks_df['Company Name'].str.contains(ent.text).sum():
                    symbol = stocks_df[stocks_df['Company Name'].str.contains(ent.text)]['Symbol'].values[0]
                    org_name = stocks_df[stocks_df['Company Name'].str.contains(ent.text)]['Company Name'].values[0]

                    stock_info = yf.Ticker(symbol+".NS").info


                    stock_info_dict['Org'].append(org_name)
                    stock_info_dict['Symbol'].append(symbol)
                    stock_info_dict['currentPrice'].append(stock_info['currentPrice'])
                    stock_info_dict['dayHigh'].append(stock_info['dayHigh'])
                    stock_info_dict['dayLow'].append(stock_info['dayLow'])
                    #stock_info_dict['forwardPE'].append(stock_info['forwardPE'])
                    #stock_info_dict['divedendYield'].append(stock_info['divedendYield'])
                else:
                    pass
            except:
                pass

    output_df = pd.DataFrame(stock_info_dict)
    return output_df


user_input = st.text_input("Add your RSS link here", "https://www.moneycontrol.com/rss/buzzingstocks.xml")

fin_headings = extract_text_from_rss(user_input)

output_df = generate_stock_info(fin_headings)
output_df.drop_duplicates(inplace=True)
st.dataframe(output_df)


with st.expander("Expand for News Headlines"):
    for heading in fin_headings:
        st.markdown("* "+ heading.text)
            








