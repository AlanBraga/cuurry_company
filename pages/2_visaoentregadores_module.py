
# librieres
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as px
import pandas as pd
import datetime
import streamlit as st
from datetime import datetime
import datetime as dt
from PIL import Image
import folium 
from streamlit_folium import folium_static 

st.set_page_config(page_title='Visão Entregadores', layout='wide')
#------------------------------------------------------
#==================== Funções ==========================
#------------------------------------------------------
def top_entregadores_lentos( df1 ):
                    
    cols = ['Delivery_person_ID', 'City', 'Time_taken(min)' ]

    top_entregadores_lentos = df1.loc[: , cols].groupby(['City', 'Delivery_person_ID']).max().sort_values( ['City', 'Time_taken(min)'] ).reset_index()

    top_entregadores_lentos1 = top_entregadores_lentos.loc[top_entregadores_lentos['City'] == 'Metropolitian', :].head(10)
    top_entregadores_lentos2 = top_entregadores_lentos.loc[top_entregadores_lentos['City'] == 'Urban', :].head(10)
    top_entregadores_lentos3 = top_entregadores_lentos.loc[top_entregadores_lentos['City'] == 'Semi-Urban', :].head(10)

    top_lentos = pd.concat ( [top_entregadores_lentos1, top_entregadores_lentos2, top_entregadores_lentos3] ).reset_index( drop=True )

    return fig

def top_entregadores_fast( df1 ):
                
    cols = ['Delivery_person_ID', 'City', 'Time_taken(min)' ]
    df_aux = df1.loc[: , cols].groupby(['City', 'Delivery_person_ID']).min().sort_values( ['City', 'Time_taken(min)'] ).reset_index()

    df_aux01 = df_aux.loc[df_aux['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df_aux.loc[df_aux['City'] == 'Urban', :].head(10)
    df_aux03 = df_aux.loc[df_aux['City'] == 'Semi-Urban', :].head(10)

    Top_10_entregadores = pd.concat ( [df_aux01, df_aux02, df_aux03] ).reset_index( drop=True )

    return fig

def mean_clima( df1 ):
            
    cols = ['Delivery_person_Ratings', 'Weatherconditions' ]
    df_aux = (df1.loc[:, cols].groupby('Weatherconditions')
  .agg({'Delivery_person_Ratings':['mean', 'std', 'min', 'max']}))

    df_aux.columns = ['delivery_mean','delivery_std','delivery_min', 'delivery_max']
    df_aux.reset_index()

    return fig
             
def avaliacao_entregador_mean( df1 ):
                    
    cols = ['Delivery_person_Ratings', 'Delivery_person_ID' ]
    df_avg_rating_por_delivery=df1.loc[:, cols].groupby('Delivery_person_ID').mean().reset_index()

    return fig

def media_transito( df1 ):
              
    cols = ['Delivery_person_Ratings', 'Road_traffic_density' ]
    df_aux = (df1.loc[:, cols].groupby('Road_traffic_density')
.agg({'Delivery_person_Ratings':['mean', "std"]}))

    df_aux.columns = ['delivery_mean','delivery_std']
    df_aux.reset_index()

    return fig
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
    default = 'Low' )

st.sidebar.markdown( """___""" )
st.sidebar.markdown( '### Powered by comunidade DS' )

#FILTRO DE DATA

linhas_selecionadas=df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de Transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas,:]

# ==========================================================
# Layout no Streamlit
# ==========================================================

tab1, tab2, yab3, = st.tabs( ['Vião Gerencial','__','__' ] )

with tab1:
    with st.container():
        st.title('Overal Metrics')
        
        col1, col2, col3, col4 = st.columns(4,gap='large')
        
        with col1:
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Maior idade', maior_idade)
            
        with col2:
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col1.metric('Maior idade', menor_idade)
            
        with col3:
            melhor_condicao = df1.loc[:, 'Vehicle_condition'].max()
            col1.metric('Melhor condição', melhor_condicao)
            
        with col4:
            pior_condicao = df1.loc[:, 'Vehicle_condition'].min()
            col1.metric('Pior condição', pior_condicao)
            
        with st.container():
            st.markdown("""___""")
            st.title('Avaliações')
            
            col1, col2, = st.columns( 2 )
            with col1:
                st.markdown('### Avaliacao medias por Entregador')
                fig = st.dataframe(df1)
                
            with col2:
                st.markdown( '### Avaliacao medias por Transito' )
                fig = st.dataframe(df1)
             
            st.markdown( '### Avaliacao medias por Clima' )
            fig = st.dataframe(df1)
            
        with st.container():
            st.markdown(' ### Velocidade de Entrega')
            
            col1, col2 = st.columns (2)
            
            with col1:
                st.markdown('### Top entregadores mais rápidos')
                fig = st.dataframe(df1)
                
            with col2:
                st.markdown('### Top entregadores mais lentos')
                fig = st.dataframe(df1)
                
                
               
                

                    
                
                
            
            
            
                
            
            
            
            
            
            
                                

                      
                      
    
    
    


