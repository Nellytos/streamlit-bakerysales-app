import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    df=pd.read_csv('Bakery sales.csv')
    df.drop('Unnamed: 0', axis=1, inplace=True)
    # df['unit_price']=df.unit_price.str.replace('[^0-9\,-]
    df['unit_price2']=df.unit_price.str.replace(',','.')
    df['unit_price2']=df.unit_price2.str.replace('€','')
    df['unit_price2']=df.unit_price2.str.strip()
    df['unit_price2']=df.unit_price2.astype('float')
    df['sales']=df.Quantity * df.unit_price2
    df.drop('unit_price', axis=1, inplace=True)
    st.write(df.shape)
    df.drop(df[df.sales == 0].index, inplace=True) # drop columns with zero sales
    # convert date column to date format
    df['date2'] = pd.to_datetime(df.date)
    st.write(df.dtypes)
    sorted_df = df.sort_values('sales', ascending=False)
    top10 = sorted_df.head(10)
    #sns.barplot(data=top10, x='article', y='sales')
    #df.to_csv() to save the cleaned data
    return df

    st.title('Demo App')

    st.subheader('Learn the basics structure')

    st.write('Bakery Sales Data')
try:    
    df = load_data()
    articles = df.article.unique()
    articles_selection = st.multiselect(
    'Choose Product', articles, [articles[0], articles[1]]
)
    articles_selected = df[df['article'].isin(articles_selection)]
    st.write(articles_selected.head())
    # st.write(df.dtypes)

    # bar chart
    st.write(''' ### Total Sales of Selected Product(s) ''')
    bar1 = articles_selected.groupby(['article'])['sales'].sum().sort_values(ascending=True)
    st.bar_chart(bar1)

    # Line chart
    st.write('''### Total Sales over Time''')
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(articles_selected['date'], articles_selected['sales'])
    st.pyplot(fig) 
                                               
    # pie chart
    st.write('''### Percentage of Selected Product(s) sold''')
    pie_data = articles_selected['article'].value_counts()
    fig2, ax2 = plt.subplots(figsize=(7,7))
    ax2.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%',shadow=True)
    ax2.axis('equal') # gives equal aspect ratio
    st.write('Note: this is showing percentages for only the values selected')
    st.pyplot(fig2)        
except ValueError as e:
    st.error('''
            Error:
            '''% e.reason)
    # st.write(df.dtypes)