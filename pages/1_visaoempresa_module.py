# librieres
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime
import streamlit as st
from datetime import datetime
import datetime as dt
from PIL import Image
import folium 

from streamlit_folium import folium_static 

st.set_page_config(page_title='Visão Empresa', layout='wide')

#------------------------------------------------------
#==================== Funções ==========================
#------------------------------------------------------

def trafiic_order( df1 ):
    #3. Distribuição dos pedidos por tipo de tráfego.
    cols = [ 'ID', 'Road_traffic_density']
    df_aux=( df1.loc[:,cols]
                .groupby('Road_traffic_density')
                .count()
                .reset_index() )

    df_aux = df_aux.loc[ df_aux['Road_traffic_density'] != 'NaN', : ] 
    df_aux['entrega_perc'] = df_aux['ID'] / df_aux['ID'].sum() 

    pie = px.pie( df_aux , values= 'entrega_perc', names='Road_traffic_density') 

    return pie
                      
def traffic_order_city( df1 ):
    #4. Comparação do volume de pedidos por cidade e tipo de tráfego.
    cols = ['ID', 'City','Road_traffic_density']
    df_aux = (df1.loc[:, cols].groupby(['City','Road_traffic_density'])
                              .count()
                              .reset_index())
    df_aux = df_aux.loc[ df_aux['City'] != 'NaN', : ] 
    df_aux = df_aux.loc[ df_aux['Road_traffic_density'] != 'NaN', : ] 

    fig2  = px.scatter( df_aux, x= 'City', y= 'Road_traffic_density' ,size='ID', color='City' )

    return fig2 
                      
def Order_by_Week( df1 ):
            
    df1['Week_Of_Year'] = df1['Order_Date'].dt.strftime('%U') # Comando de Criação
                      
    df_aux01 =( df1.loc[:, ['ID','Week_Of_Year']]
                   .groupby('Week_Of_Year')
                   .count()
                   .reset_index() )

    df_aux02 =( df1.loc[:, ['Delivery_person_ID', 'Week_Of_Year']]
                   .groupby('Week_Of_Year')
                   .nunique()
                   .reset_index())

    df_aux = pd.merge( df_aux01, df_aux02, how= 'inner' )
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']

    fig = px.line( df_aux , x= 'Week_Of_Year', y='order_by_deliver')

    return fig
                      
def Order_Share_by_Week( df1 ):
        
    df1['Week_Of_Year'] = df1['Order_Date'].dt.strftime('%U') # Comando de Criação
                      
    cols = [ 'ID', 'Week_Of_Year']

    df_aux =( df1.loc[:, cols ]
                 .groupby('Week_Of_Year')
                 .count()
                 .reset_index() )

    fig = px.line( df_aux , x= 'Week_Of_Year', y='ID')

    return fig
                      
def Country_Map(df1):
    map = folium.Map()

    for index, row in df1.iterrows():
        popup_info = {
            'City': row['City'],
            'Road_traffic_density': row['Road_traffic_density']
        }

        folium.Marker([row['Delivery_location_latitude'], row['Delivery_location_longitude']],
                      popup=str(popup_info)).add_to(map)

    folium_static(map, width=1024, height=600)

    return None                  

def clean_code( df1 ):
    
    ''' Esta funcção tem a responsabilidade de limpeza dp dataframe
        
        1- Remoção dos NaN
        2- Mudança do tipo da coluna de dados
        3- Remoção dos espaços das variáveis de texto
        4- formatação da coluna de datas
        5- limpeza da coluna de tempo ( remoção do texyo da variável númerica )
        
        Input :  dataframe
        output: dataframe
    '''
    #1. removendo os os NAN da coluna 'Delivery_person_Age' e 'multiple_deliveries'
    linhas_selecionadas = df1['Delivery_person_Age'] != 'NaN ' # 
    df1 = df1.loc[linhas_selecionadas, :].copy() # 
    linhas_selecionadas = df1['multiple_deliveries'] != 'NaN ' 
    df1 = df1.loc[linhas_selecionadas, :].copy()

    #2. convertendo multiple_delivereies de texto para numero inteiro ( int )
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )
    
    #3. convertendo coluna 'Delivery_person_Ratings' para float
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )
    
    #4. convertendo a coluna order_date de texto para data
    df1['Order_Date'] = pd.to_datetime( df['Order_Date'], format='%d-%m-%Y' )
    
    #5. Removendo os espaços dentro de strings/text/object
    df1.loc[:,'ID'] = df1.loc[:,'ID'].str.strip()
    df1.loc[:,'Delivery_person_ID'] = df1.loc[:,'Delivery_person_ID'].str.strip()
    df1.loc[:,'Road_traffic_density'] = df1.loc[:,'Road_traffic_density'].str.strip()
    df1.loc[:,'Type_of_order'] = df1.loc[:,'Type_of_order'].str.strip()
    df1.loc[:,'Type_of_vehicle'] = df1.loc[:,'Type_of_vehicle'].str.strip()
    df1.loc[:,'City'] = df1.loc[:,'City'].str.strip()
    
    #6. limpando a coluna de time taken
    df1["Time_taken(min)"] = df1["Time_taken(min)"].apply(lambda x: x.split("(min)")[-1] if len(x.split("(min)")) > 1 else x)
    
    #7. convertendo 'Time_taken(min)' de texto para numero inteiro ( int )
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )
    
    return df1

# ------------------------- Ínicio da Estrutura Lógica dos códigos-----------------

# -------------------------
# import daset
# -------------------------

df = pd.read_csv('datascincie/train.csv')

# -------------------------
# limpando dados
# -------------------------

df1 = clean_code( df )

# ==========================================================
# Barra Lateral
# ==========================================================


st.header('Marketplace - Visão')

image_path = 'logo.png'
image = Image.open( image_path )
st.sidebar.image( image, width=120 )

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""___""")

st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider(
    'Até qual Valor?',
    value=dt.datetime(2022, 4, 13),
    min_value=dt.datetime(2022, 2, 11),
    max_value=dt.datetime(2022, 4, 6),
    format='DD-MM-YYYY' )
st.sidebar.markdown( """___""" )

traffic_options=st.sidebar.multiselect(
    'Quais as condições do transito?',
    ['Low', 'Medium', 'High', 'Jam'],
    default = ['Low', 'Medium', 'High', 'Jam'] )

st.sidebar.markdown( """___""" )
st.sidebar.markdown( '### Powered by comunidade DS' )

#FILTRO DE DATA

linhas_selecionadas=df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de Transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas,:]



st.dataframe(df1)

# ==========================================================
# Layout no Streamlit
# ==========================================================

tab1, tab2, tab3 = st.tabs([ 'Visão Gerencial','Visão Tática','Visão Geografica'])

with tab1:
    with st.container():
        #1. Order_matric
        cols = [ 'ID', 'Order_Date']
        df_aux = df1.loc[:, cols ].groupby('Order_Date').count().reset_index()
        #df_aux.head()
        fig1 = px.bar( df_aux , x= 'Order_Date', y='ID')  
        st.plotly_chart( fig1, use_container_width=True )
        
        
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.header('Traffic Order Share')
            fig = trafiic_order( df1 )
            st.plotly_chart( fig, use_container_width=True ) 
         
        with col2:
            fig2  = traffic_order_city( df1 )
            st.header('Traffic Order City')          
            st.plotly_chart( fig2, use_container_width=True )          
           

        
        
with tab2:
    with st.container():
        st.markdown("# Order by Week")              
        fig = Order_by_Week( df1 )              
        st.plotly_chart( fig, use_container_width=True ) 
                 
    
    with st.container():
        st.markdown("# Order Share by Week")
        fig = Order_Share_by_Week( df1 )
        st.plotly_chart(fig, use_container_width = True)

        
        
with tab3:
    st.markdown("#Country Map")
    Country_Map( df1 )