import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(layout='wide', page_title='Startup Analysis')

df = pd.read_csv(r"G:\Campusx\pandas\startup_cleaned.csv")
df['date'] = pd.to_datetime(df.date, errors='coerce')
df['month'] = df.date.dt.month
df['year'] = df.date.dt.year


def load_overall_analysis():
    st.title('Overall Analysis')

    # total invested amount
    total = round(df.amount.sum())

    # max amount infused in a startup
    max_funding = df.groupby('startup').amount.max().sort_values(ascending=False).values[0]

    # avg ticket size
    avg_funding = round(df.groupby('startup').amount.sum().mean())

    # total funded startups
    num_startups = df.startup.nunique()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total', str(total) + " Cr")
    with col2:
        st.metric('Max', str(max_funding) + " Cr")
    with col3:
        st.metric('Avg', str(avg_funding) + " Cr")
    with col4:
        st.metric('Funded Startups', num_startups)

    st.header("MoM Graph")
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])

    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month']).amount.sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month']).amount.count().reset_index()

    temp_df['x_axis'] = temp_df.month.astype('str') + "-" + temp_df.year.astype('str')

    fig0, ax0 = plt.subplots()
    ax0.plot(temp_df['x_axis'], temp_df['amount'])

    st.pyplot(fig0)


def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investments of the investors
    last5_df = df[df.investors.str.contains(investor)].head()[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
        # biggest investments
        big_ser = df[df.investors.str.contains(investor)].groupby('startup')['amount'].sum()\
            .sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_ser.index, big_ser.values)

        st.pyplot(fig)

    with col2:
        vertical_ser = df[df.investors.str.contains(investor)].groupby('vertical')\
            .amount.sum()

        st.subheader('Sectors Invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_ser, labels=vertical_ser.index, autopct="%0.01f%%")

        st.pyplot(fig1)

    col3, col4 = st.columns(2)
    with col3:
        round_ser = df[df.investors.str.contains(investor)].groupby('round') \
            .amount.sum()

        st.subheader('Stage of Funding')
        fig2, ax2 = plt.subplots()
        ax2.pie(round_ser, labels=round_ser.index, autopct="%0.01f%%")

        st.pyplot(fig2)

    with col4:
        city_ser = df[df.investors.str.contains(investor)].groupby('city') \
            .amount.sum()

        st.subheader('City Wise Investments')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_ser, labels=city_ser.index, autopct="%0.01f%%")

        st.pyplot(fig3)

    col5, col6 = st.columns(2)
    with col5:
        df['year'] = df.date.dt.year
        year_ser = df[df.investors.str.contains(investor)].groupby('year').amount.sum()

        st.subheader('YoY Investment')
        fig4, ax4 = plt.subplots()
        ax4.plot(year_ser.index, year_ser.values)

        st.pyplot(fig4)

    with col6:
        # 5 similar investor
        inv_df = df[df.investors.str.contains(investor)]
        common_inv_ser = pd.Series(inv_df.investors.str.split(',')
                                   .sum()).value_counts().iloc[1:].head()
        common_inv_ser.index.name = 'Investors List'
        st.subheader('Similar Investors')
        st.dataframe(common_inv_ser.index, width=720, hide_index=True)


st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()
elif option == 'Startup':
    st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique()))
    bt1 = st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')
else:
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df.investors.str.split(',').sum())))
    bt2 = st.sidebar.button('Find Investor Details')
    if bt2:
        load_investor_details(selected_investor)
    st.title('Investor Analysis')

