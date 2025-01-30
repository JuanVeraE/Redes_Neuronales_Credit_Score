import streamlit as st
import pandas as pd
import joblib
from model import modelo
from grafica import create_gauge
import numpy as np

# Cargar el MinMaxScaler guardado
scaler = joblib.load('minmax_scaler.pkl')  # Asegúrate de tener el archivo 'minmax_scaler.pkl' en el directorio adecuado

# Función para preprocesar los datos
def preprocess_data(data):
    # Cargar las columnas categóricas
    categorical_columns = ["initial_list_status", "grade", "sub_grade", "purpose", "home_ownership"]

    print(data)
    # Aplicar codificación one-hot
    data = pd.get_dummies(data, columns=categorical_columns, drop_first=False)
    print(data)

    # Para asegurarnos de que todas las columnas estén presentes, cargamos el conjunto original de columnas de las variables categóricas
    # Si tienes un DataFrame original con todas las posibles columnas, puedes obtener las columnas en esta forma:
    data_dummies = {
        'initial_list_status': ['f', 'w'],
        'grade': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'sub_grade': ['B2', 'C4', 'C5', 'C1', 'B5', 'A4', 'E1', 'F2', 'C3', 'B1', 'D1', 'A1', 'B3', 'B4',
                      'C2', 'D2', 'A3', 'A5', 'D5', 'A2', 'E4', 'D3', 'D4', 'F3', 'E3', 'F4', 'F1', 'E5', 'G4',
                      'E2', 'G3', 'G2', 'G1', 'F5', 'G5'],
        'purpose': ['credit_card', 'car', 'small_business', 'other', 'wedding', 'debt_consolidation',
                    'home_improvement', 'major_purchase', 'medical', 'moving', 'vacation', 'house',
                    'renewable_energy', 'educational'],
        'home_ownership': ['RENT', 'OWN', 'MORTGAGE', 'OTHER', 'NONE', 'ANY']
    }

    # Crear un DataFrame con todas las categorías
    df_dummies = pd.DataFrame({col: pd.Series(values) for col, values in data_dummies.items()})
    original_columns = pd.get_dummies(df_dummies, drop_first=False)

    # Obtener las columnas en un DataFrame de todas las posibles combinaciones de categorías
    all_columns = list(original_columns.columns)

    print(all_columns)


    # Escalar las columnas numéricas
    final_columns = ['annual_inc', 'out_prncp', 'out_prncp_inv',
       'total_pymnt', 'total_pymnt_inv', 'total_rec_prncp', 'last_pymnt_amnt',
       'tot_cur_bal', 'initial_list_status_f', 'initial_list_status_w',
       'grade_A', 'grade_B', 'grade_C', 'grade_D', 'grade_E', 'grade_F',
       'grade_G', 'sub_grade_A1', 'sub_grade_A2', 'sub_grade_A3',
       'sub_grade_A4', 'sub_grade_A5', 'sub_grade_B1', 'sub_grade_B2',
       'sub_grade_B3', 'sub_grade_B4', 'sub_grade_B5', 'sub_grade_C1',
       'sub_grade_C2', 'sub_grade_C3', 'sub_grade_C4', 'sub_grade_C5',
       'sub_grade_D1', 'sub_grade_D2', 'sub_grade_D3', 'sub_grade_D4',
       'sub_grade_D5', 'sub_grade_E1', 'sub_grade_E2', 'sub_grade_E3',
       'sub_grade_E4', 'sub_grade_E5', 'sub_grade_F1', 'sub_grade_F2',
       'sub_grade_F3', 'sub_grade_F4', 'sub_grade_F5', 'sub_grade_G1',
       'sub_grade_G2', 'sub_grade_G3', 'sub_grade_G4', 'sub_grade_G5',
       'purpose_car', 'purpose_credit_card', 'purpose_debt_consolidation',
       'purpose_educational', 'purpose_home_improvement', 'purpose_house',
       'purpose_major_purchase', 'purpose_medical', 'purpose_moving',
       'purpose_other', 'purpose_renewable_energy', 'purpose_small_business',
       'purpose_vacation', 'purpose_wedding', 'home_ownership_ANY',
       'home_ownership_MORTGAGE', 'home_ownership_NONE',
       'home_ownership_OTHER', 'home_ownership_OWN', 'home_ownership_RENT']
    data = data.reindex(columns=final_columns, fill_value=0)
    data = scaler.transform(data)[0]
    data = np.array([data])

    respuesta = int(modelo.predict(data)[0][0] * 100)

    return respuesta

# Título de la app
st.title("Formulario de Preprocesamiento de Datos")

# Crear formulario en Streamlit
with st.form("input_form"):
    grade = st.selectbox("Grade", ['B', 'C', 'A', 'E', 'F', 'D', 'G'])
    sub_grade = st.selectbox("Sub Grade", ['B2', 'C4', 'C5', 'C1', 'B5', 'A4', 'E1', 'F2', 'C3', 'B1', 'D1', 'A1', 'B3',
                                          'B4', 'C2', 'D2', 'A3', 'A5', 'D5', 'A2', 'E4', 'D3', 'D4', 'F3', 'E3', 'F4',
                                          'F1', 'E5', 'G4', 'E2', 'G3', 'G2', 'G1', 'F5', 'G5'])
    home_ownership = st.selectbox("Home Ownership", ['RENT', 'OWN', 'MORTGAGE', 'OTHER', 'NONE', 'ANY'])
    annual_inc = st.number_input("Annual Income", min_value=0.0)
    purpose = st.selectbox("Purpose", ['credit_card', 'car', 'small_business', 'other', 'wedding', 'debt_consolidation',
                                      'home_improvement', 'major_purchase', 'medical', 'moving', 'vacation', 'house',
                                      'renewable_energy', 'educational'])
    initial_list_status = st.selectbox("Initial List Status", ['f', 'w'])
    out_prncp = st.number_input("Outstanding Principal", min_value=0.0)
    out_prncp_inv = st.number_input("Outstanding Principal Investment", min_value=0.0)
    total_pymnt = st.number_input("Total Payment", min_value=0.0)
    total_pymnt_inv = st.number_input("Total Payment Investment", min_value=0.0)
    total_rec_prncp = st.number_input("Total Recovered Principal", min_value=0.0)
    last_pymnt_amnt = st.number_input("Last Payment Amount", min_value=0.0)
    tot_cur_bal = st.number_input("Total Current Balance", min_value=0.0)

    # Botón para enviar el formulario
    submit_button = st.form_submit_button("Preprocesar y mostrar datos")

# Si el formulario fue enviado
if submit_button:
    # Crear un DataFrame con los datos ingresados
    input_data = {
        'grade': [grade],
        'sub_grade': [sub_grade],
        'home_ownership': [home_ownership],
        'annual_inc': [annual_inc],
        'purpose': [purpose],
        'initial_list_status': [initial_list_status],
        'out_prncp': [out_prncp],
        'out_prncp_inv': [out_prncp_inv],
        'total_pymnt': [total_pymnt],
        'total_pymnt_inv': [total_pymnt_inv],
        'total_rec_prncp': [total_rec_prncp],
        'last_pymnt_amnt': [last_pymnt_amnt],
        'tot_cur_bal': [tot_cur_bal]
    }

    # Convertir a DataFrame
    input_df = pd.DataFrame(input_data)

    # Preprocesar los datos
    resultado = preprocess_data(input_df)

    st.write("Datos Preprocesados")
    fig = create_gauge(resultado)
    st.pyplot(fig)
