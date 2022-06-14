import pandas as pd
import streamlit as st
import folium
import numpy as np
from streamlit_folium import folium_static
import plotly.express as px


st.set_page_config(layout='wide')


@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)
    return data


    return geofile


def remove_duplicates(data):
    data = data.drop_duplicates(subset = ['id'], keep = 'last')
    return data

def remove_value(data):
    data = data.drop(15870)
    return data

def set_feature(data):
    data['price_m2'] = data['price'] / data['sqft_lot']

    return data

def data_overview(data):
    if st.checkbox('Mostrar os Conjunto de Dados'):
        

        f_attributes = st.sidebar.multiselect('Enter columns', data.columns)
        f_zipcode = st.sidebar.multiselect('Enter Zipcode', data['zipcode'].unique())
    
        if (f_zipcode != [] ) & (f_attributes != []):
            data = data.loc[data['zipcode'].isin(f_zipcode), f_attributes]

        elif (f_zipcode != [] ) & (f_attributes == []):
            data = data.loc[data['zipcode'].isin(f_zipcode), :]

        elif (f_zipcode == [] ) & (f_attributes != []):
            data = data.loc[:, f_attributes]

        else:
            data = data.copy()

        st.write(data.head(50))

    st.sidebar.title('House Rocket')
    st.sidebar.write('A House Rocket trabalha no ramo de venda e compra de imóveis.'
                     'Para encontrar as melhores oportunidades, a empresa conta com uma'
                     'equipe de cientista de dados, para apresentar as melhores escolhas para empresa.')
    st.sidebar.write('As informações do projeto podem ser acessadas através do seguinte link:')
    
    st.sidebar.write("Para mais informações sobre o projeto, acesse: "
                         "[GitHub](https://https://github.com/carlosandradeds/house-rocket)")

    return None

def avg_metrics(data):
    if st.checkbox('Avg metrics'):

        df1 = data[['id', 'zipcode']].groupby('zipcode').count().reset_index()
        df2 = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
        df3 = data[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
        df4 = data[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()

        #merge
        m1 = pd.merge(df1, df2, on='zipcode', how='inner')
        m2 = pd.merge(m1, df3, on='zipcode', how='inner')
        df = pd.merge(m2, df4, on='zipcode', how='inner')

        df.columns = ['ZIPCODE', 'TOTAL HOUSES', 'PRICE', 'SQRT_LIVING', 'PRICE/M2']

        st.header('Average Values')
        st.dataframe(df, height=600)

    return None


def statistic_descriptive(data):
    if st.checkbox('Statistic descriptive'):

        num_attributes = data.select_dtypes(include=['int64', 'float64'])
        media_ = pd.DataFrame(num_attributes.apply(np.mean))
        median_ = pd.DataFrame(num_attributes.apply(np.median))
        std_ = pd.DataFrame(num_attributes.apply(np.std))

        max_ = pd.DataFrame(num_attributes.apply(np.max))
        min_ = pd.DataFrame(num_attributes.apply(np.min))

        df1 = pd.concat([max_, min_, media_, median_, std_], axis=1).reset_index()

        df1.columns  = ['attributes', 'max', 'min', 'mean', 'median', 'std']
        
        st.header('Descriptive Analysis')
        st.dataframe(df1, height=800)

    return None

def assumptions(data):

    c1, c2 = st.columns((1,1))
    
    
    #H1
    c1.header('H1 - Imoveis que possuem vista para água, são 30% mais caros, na média.')
    by_waterfront = data[['waterfront', 'price']].groupby('waterfront').mean().reset_index()
    fig = px.bar(by_waterfront, x='waterfront', y='price', color='waterfront')
    c1.plotly_chart(fig, use_container_width=True)


    #H2
    c2.header('H2 - Imóveis com data de construção menor que 1955, são 50% mais baratos, na média.')
    data['old-new'] = data['yr_built'].apply(lambda x: '> 1955' if
                                             x > 1955 else '< 1955')
    h2 = data[['old-new','price']].groupby('old-new').mean().reset_index()
    fig2 = px.bar(h2, x='old-new', y='price', color = 'old-new')
    c2.plotly_chart(fig2, use_container_width=True)

    #H3
    c3, c4 = st.columns(2)
    c3.header('H3 - Imóveis com porão são em média 20% mais caros')
    data['porao'] = data['sqft_basement'].apply(lambda x: 'não' if x == 0
                                                else 'sim')    
    
    h3 = data[['porao', 'price']].groupby('porao').mean().reset_index()
    fig3 = px.bar(h3, x='porao', y='price', color='porao')
    c3.plotly_chart(fig3, use_container_width=True)


    #H4
    c4.header('H4 - O crescimento do preço dos imóveis MoM em 2015 é de 10%')
    data['date'] = pd.to_datetime(data['date'])

    data['month'] = data['date'].dt.month
    data['year'] = data['date'].dt.year

    year_data = data[data['year'] == 2014]

    h4 = year_data[['month', 'price', 'sqft_lot']].groupby('month').sum().reset_index()
    fig4 = px.line(h4, x='month', y='price', color_discrete_sequence=['teal'], template='simple_white')

    c4.plotly_chart(fig4, use_container_width=True)

    #H5
    c5, c6 = st.columns(2)
    c5.header('H5 - Imóveis com maior numero de banheiros são 10% mais caros.')
    h5 = data[['bathrooms', 'price']].groupby('bathrooms').mean().reset_index()
    fig5 = px.bar(h5, x='bathrooms', y='price', color='bathrooms')

    c5.plotly_chart(fig5, use_container_width=True)

    #H6
    c6.header('H6 - Imóveis que nunca foram reformados são 20% mais baratos que imóveis que já foram reformados')
    data['renovation'] = data['yr_renovated'].apply(lambda x: 'não' if x == 0
                                                    else 'sim')

    h6 = data[['renovation', 'price']].groupby('renovation').mean().reset_index()
    fig6 = px.bar(h6, x='renovation', y='price', color='renovation')
    c6.plotly_chart(fig6, use_container_width=True)

    #H7
    c7, c8 = st.columns(2)
    c7.header('H7 - Imóveis que estão no centro da cidade são 30% mais caros.')
    h7 = data[['zipcode', 'price']].groupby('zipcode').median().reset_index()
    fig7 = px.bar(h7, x='zipcode', y='price', color='zipcode')
    c7.plotly_chart(fig7, use_container_width=True)



    #H8
    c8.header('H8 - Imóveis são 10% mais bem vendidos no verão.')
    data['season'] = data['month'].apply(lambda x: 'summer' if (x > 5) & (x < 8) else
                                         'spring' if (x > 2) & (x < 5) else
                                         'fall' if (x > 8) & (x < 12) else
                                         'winter')
        
    h8 = data[['season', 'price']].groupby('season').sum().reset_index()
    fig8 = px.bar(h8, x='season', y='price', color='season')
    c8.plotly_chart(fig8, use_container_width=True)


    #H9
    c9, c10 = st.columns(2)
    c9.header('H9 - Imóveis com más condições, não renovados, são 40% mais baratos')
    data_mask = data['renovation'] == 'não'
    filtered = data[data_mask]
    filtered['condição'] = filtered['condition'].apply(lambda x: 'bad' if x < 3 else
                                               'good' if x == 3 else
                                               'excellent')

    h9 = filtered[['condição', 'price']].groupby('condição').mean().reset_index()
    fig9 = px.bar(h9, x='condição', y='price', color='condição')
    c9.plotly_chart(fig9, use_container_width=True)

    #H10
    c10.header('H10 - Imóveis com qualidade de vista mais alta tem valor 20% mais caro')
    h10 = data[['view', 'price']].groupby('view').mean().reset_index()
    fig10 = px.bar(h10, x='view', y='price', color='view')
    c10.plotly_chart(fig10, use_container_width=True)
    
    
    
    
    return None

def answer(data):
    st.markdown("<h1 style='text-align: center; color: black;'> Questões de Negócio</h1>", unsafe_allow_html=True)
    st.subheader('1. Quais são os imóveis que a House Rocket deveria comprar e por qual preço?')

    a = data[['zipcode', 'price']].groupby('zipcode').median().reset_index()

    df2 = pd.merge(a, data, on='zipcode',how='inner')

    df2 = df2.rename(columns={'price_x': 'price_median', 'price_y': 'price'})

    for i, row in df2.iterrows():
      if (row['price_median'] >= row['price']) & (row['condition'] < 3) & (row['renovation'] == 'não'):
        df2.loc[i, 'pay'] = 'sim'
      else:
        df2.loc[i, 'pay'] = 'não'

    compra = df2[df2['pay'] == 'sim']

    st.write(compra[['id', 'price', 'zipcode']] )

    for i, row in df2.iterrows():
        if (row['pay'] == 'sim'):
            df2.loc[i, 'marker_color'] = 'green'
        else:
            df2.loc[i, 'marker_color'] = 'red'

    st.markdown('Mapa - Quais imóveis devem ser comprados?')
    st.markdown("""
        <style>
        .big-font {
         font-size:14px !important;
     }
     </style>
        """, unsafe_allow_html=True)

    st.markdown('<p class="big-font"> Em verde os imóveis indicados '
                    'para compra  <br> Em vermelho os imóveis não indicados para compra </p>', unsafe_allow_html=True)
    
    
    st.markdown('<p class="big-font"> No canto superior direito do mapa, mini-menu para marcar as opções', unsafe_allow_html=True)

    mapa = folium.Map(width=600, height = 300,
                      location = [data['lat'].mean(), data['long'].mean()],
                      default_zoom_start = 30)

    features = {}
    for row in pd.unique(df2['marker_color']):
        features[row] = folium.FeatureGroup(name=row)

    for index, row in df2.iterrows():
        circ = folium.Circle([row['lat'], row['long']], radius=150,
                             color=row['marker_color'], fill_color=row['marker_color'],
                             fill_opacity = 1, popup='Compra {}, preço {}'.format(row['pay'], row['price']))

        circ.add_to(features[row['marker_color']])

    for row in pd.unique(df2['marker_color']):
        features[row].add_to(mapa)

    folium.LayerControl().add_to(mapa)
    folium_static(mapa)
    
    
    # questão 2
    st.subheader('2. Uma vez comprado, qual é o melhor momento para vendê-lo e por qual preço?')
    df3 = df2.copy()

    df3['season'] = df3['month'].apply(lambda x: 'summer' if (x > 5) & (x < 8) else
                                               'spring' if (x > 2) & (x < 5) else
                                               'fall' if (x > 8) & (x < 12) else
                                               'winter')

    df3 = df3[df3['pay'] == 'sim']
    df4 = df3[['season', 'zipcode', 'price']].groupby(['zipcode', 'season']).median().reset_index()

    df4 = df4.rename(columns = {'price' : 'price_medi_season', 'season': 'season_median'} )

    df5 = pd.merge(df3, df4, on='zipcode', how = 'inner')

    for i, row in df5.iterrows():
        if (row['price_medi_season'] > row['price']):
            df5.loc[i, 'sale'] =  row['price'] * 0.1
        else:
            df5.loc[i, 'sale'] = row['price'] * 0.3


    df5= df5[['price_medi_season', 'price', 'sale', 'price_median', 'season', 'zipcode']]


    fig11 = px.bar(df5, x = 'season', y = 'sale', color = 'season', labels={'season':'Estação do Ano', 'sale': 'Preço de Venda'},
                                                                        template = 'simple_white')
    fig11.update_layout(showlegend = False)
    st.plotly_chart(fig11, x='season', y='sale', use_container_width= True)
    return None

def tabela (data):
    st.markdown("<h1 style='text-align: center; color: black;'> Resumo sobre as Hipóteses </h1>", unsafe_allow_html=True)
    hipoteses = pd.DataFrame({
    '.': ['Verdadeiro', 'Falso', 'Verdadeiro', 'Falso', 'Falso', 'Verdadeiro', 'Verdadeiro', 'Falso', 'Verdadeiro', 'Verdadeiro']}, index=['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10'])
    hipoteses = hipoteses.style.set_table_styles([dict(selector='th', props=[('text-align', 'center')])])
    hipoteses.set_properties(**{'text-align': 'center'}).hide_index()
    st.table(hipoteses)
    return None


if __name__ == '__main__':
    path = 'kc_house_data.csv'
    data = get_data(path)

    remove_duplicates(data)

    remove_value(data)
    
    data = set_feature(data)
    
    data_overview(data)

    avg_metrics(data)

    statistic_descriptive(data)

    assumptions(data)

    answer(data)

    tabela(data)


    
    
