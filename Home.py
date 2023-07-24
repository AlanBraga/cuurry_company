import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon=""
    
)

image_path = 'logo.png'
image = Image.open( image_path )
st.sidebar.image( image, width=120 )

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""___""")

st.write("# Curry Company Grouth Dashboard")

st.markdown(
    
    """
    Group Dashboard foi contruido para acompanhar as métricsa de crescimento dos entregadores e restaurantes.
    ### Como utilizar esse Dashboard?
    - Visão Empresa:
        - Visão Gerencial : métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Gerográfica: Insigths de geolocalização.
    - Visão Entregador: 
        - Acompanhamento dos inicadores semanais de crescimento.
    - Visão Restaurante: Indicadores semanais de crescimento dos Restaurantes.
    ### Ask for Help:
    - Time de Data Science no discord
        -@meigarom
        
""")

        
        
            