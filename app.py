from

import streamlit as st

st.title('DataCredito: Averigua es tu puntaje crediticio')

st.write('En el siguiente formulario ingrese los datos solicitados')

with st.form('my_form'):
    cedula = st.text_input('Cédula')
    ing_anual = st.number_input('Ingreso anual')
    ing_ult_mes = st.number_input('Ingreso último mes')
    objetivo = st.selectbox('Objetivo', ['Compra de vivienda', 'Compra de vehículo', 'Compra de electrodomésticos', 'Compra de tecnología', 'Compra de muebles', 'Viaje', 'Educación', 'Otro'])
    st.form_submit_button('Submit')

st.write('Gauge Chart')
st.write('El siguiente gráfico muestra el puntaje crediticio del usuario')
st.image('gauge_chart.png', use_column_width=True)

