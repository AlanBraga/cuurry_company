
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
import numpy as np

st.set_page_config(page_title='Visão Restaurantes', layout='wide')
#------------------------------------------------------
#==================== Funções ==========================
#------------------------------------------------------
            
def distance_mean(df1):
    cols = ['Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']
    df1['Distance'] = df1.loc[ : , cols].apply( lambda x:
                    haversine(
                        ( x['Restaurant_latitude'], x['Restaurant_longitude'] ),
                        ( x['Delivery_location_latitude'], x['Delivery_location_longitude'] ) ), axis=1 )

    distance_mean = np.round( df1.loc[:, 'Distance'].mean(), 2)

    
    return distance_mean

def tempo_medio(df1):
    colus = ['Time_taken(min)', 'Festival']
    df_aux = (df1.loc[:, colus].groupby('Festival')
  .agg({'Time_taken(min)':['mean', 'std']}) )

    df_aux.columns = ['Tempo_mean', 'Tempo_std']
    df_aux = df_aux.reset_index()

    linhas_selecionadas = df_aux['Festival'] == 'Yes '
    tempo_medio = np.round(df_aux.loc[linhas_selecionadas, 'Tempo_mean' ], 2)

    return tempo_medio

            
def desvio_padrao(df1):
    colus = ['Time_taken(min)', 'Festival']
    df_aux = (df1.loc[:, colus].groupby('Festival')
  .agg({'Time_taken(min)':['mean', 'std']}) )

    df_aux.columns = ['Tempo_mean', 'Tempo_std']
    df_aux = df_aux.reset_index()

    linhas_selecionadas = df_aux['Festival'] == 'Yes '
    desvio_padrao = np.round(df_aux.loc[linhas_selecionadas, 'Tempo_std' ], 2)
    
    return desvio_padrao

def avg_time(df1):
    colus = ['Time_taken(min)', 'Festival']

    df_aux = (df1.loc[:, colus].groupby('Festival')
  .agg({'Time_taken(min)':['mean', 'std']}) )

    df_aux.columns = ['Tempo_mean', 'Tempo_std']
    df_aux = df_aux.reset_index()

    linhas_selecionadas = df_aux['Festival'] == 'No '
    avg_time = np.round(df_aux.loc[linhas_selecionadas, 'Tempo_mean' ], 2)

    col5.metric('Tempo médio S/ Festival', avg_time)

    return avg_time

def std_padrao(df1):
    colus = ['Time_taken(min)', 'Festival']

    df_aux = (df1.loc[:, colus].groupby('Festival')
  .agg({'Time_taken(min)':['mean', 'std']}) )

    df_aux.columns = ['Tempo_mean', 'Tempo_std']
    df_aux = df_aux.reset_index()

    linhas_selecionadas = df_aux['Festival'] == 'No '
    std_padrao = np.round(df_aux.loc[linhas_selecionadas, 'Tempo_std' ], 2)

    return std_padrao



def avg_std_city(df1):
    df_aux = (df1.loc[ : , ['City','Time_taken(min)']].groupby( 'City' ).agg({ 'Time_taken(min)': [ 'mean' , 'std' ]}) )

    df_aux.columns = [ 'avg_time' , 'std_time' ]
    df_aux = df_aux.reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar( name='control', x=df_aux[ 'City' ], y=df_aux['avg_time'], error_y=dict( type='data', array=df_aux['std_time'] ) ) ) 
    fig.update_layout(barmode='group')

    return fig

def avg_std_time_on_traffic(df1):
            
    colus = ['Time_taken(min)', 'City', 'Road_traffic_density']

    df_aux = (df1.loc[:, colus].groupby(['City', 'Road_traffic_density'])
              .agg({'Time_taken(min)':['mean', 'std']}) )

    df_aux.columns = [ 'avg_time' , 'std_time' ]
    df_aux = df_aux.reset_index()

    fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time', color='std_time', color_continuous_scale='RdBu', color_continuous_midpoint=np.average(df_aux['std_time']))

    return fig

def avg_std_distance(df1):
    colus = ['Time_taken(min)', 'City', 'Type_of_order']

    df_aux = (df1.loc[:, colus].groupby(['City', 'Type_of_order'])
              .agg({'Time_taken(min)':['mean', 'std']}) )

    df_aux.columns = ['Time_taken_mean','Time_taken_std']
    avg_std_distance = df_aux.reset_index()

    return avg_std_distance
               
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
    linhas_selecionadas = df1['City'] != 'NaN ' 
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

# ==========================================================
# Layout no Streamlit
# ==========================================================

tab1, tab2, tab3 = st.tabs(['Visão Gerencial','_','_'])

with tab1:
    with st.container():
        st.title("Overal Metrics")
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            Deliveri_entregadores_unicos = len ( df1.loc [:,'Delivery_person_ID' ].unique())
            col1.metric('Entregadores', Deliveri_entregadores_unicos)
            
        with col2:
            distance_mean = distance_mean(df1)
            col2.metric('Distancia Média',distance_mean )

        with col3:
            tempo_medio = tempo_medio(df1)
            col3.metric('Tempo médio C/ Festival', tempo_medio)
            
        with col4:
            desvio_padrao = desvio_padrao(df1)
            col4.metric('Desvio Padrão C/ Festival', desvio_padrao)

        with col5:
            avg_time = avg_time(df1)
            col5.metric('Tempo médio S/ Festival', avg_time)
            
        with col6:
            std_padrao = std_padrao(df1)
            col6.metric('Desvio Padrão  S/ Festival', std_padrao)
     
      
    with st.container():
        st.markdown("""___""")
        st.title("Tempo de entrega por cidade")

        df1['distance'] = df1.loc[ : ,['Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']].apply( lambda x:
                            haversine(
                                ( x['Restaurant_latitude'], x['Restaurant_longitude'] ),
                                ( x['Delivery_location_latitude'], x['Delivery_location_longitude'] ) ), axis=1 )

        avg_distance = df1.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()
        fig = go.Figure( data=[go.Pie(labels=avg_distance['City'], values=avg_distance['distance'], pull=[0.05,0, 0, 0])])
        st.plotly_chart(fig)
     
    with st.container():
        st.markdown("""___""")
        st.title("Distribuição do tempo")
       
        col1, col2 = st.columns(2)
       
        with col1:
            st.markdown("""___""")
                      
            fig = avg_std_city(df1)
            st.plotly_chart( fig )
     
        with col2:
            st.markdown("""___""")
            fig = avg_std_time_on_traffic(df1)
            st.plotly_chart( fig )
            
    with st.container():
        st.markdown("""___""")
        st.title("Distribuição da Distancia")
        avg_std_distance = avg_std_distance(df1)
        st.write(avg_std_distance)

        
        
        

            
     
            
            
        
                
                
               
                

                    
                
                
            
            
            
                
            
            
            
            
            
            
                                

                      
                      
    
    
    


