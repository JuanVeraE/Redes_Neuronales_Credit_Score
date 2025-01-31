import streamlit as st
import pandas as pd
import joblib
from model import modelo
from grafica import create_gauge
import numpy as np

# Cargar el MinMaxScaler guardado
scaler = joblib.load('minmax_scaler_new.pkl')  # Asegúrate de tener el archivo 'minmax_scaler.pkl' en el directorio adecuado

# Función para preprocesar los datos
def preprocess_data(data):
    # Cargar las columnas categóricas
    categorical_columns = ["grade", "home_ownership", "purpose"]

    print(data)
    # Aplicar codificación one-hot
    data = pd.get_dummies(data, columns=categorical_columns, drop_first=False)
    print(data)

    # Para asegurarnos de que todas las columnas estén presentes, cargamos el conjunto original de columnas de las variables categóricas
    # Si tienes un DataFrame original con todas las posibles columnas, puedes obtener las columnas en esta forma:
    data_dummies = {
        'grade': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'home_ownership': ['RENT', 'OWN', 'MORTGAGE', 'OTHER', 'NONE', 'ANY'],
        'purpose': ['credit_card', 'car', 'small_business', 'other', 'wedding', 'debt_consolidation',
                    'home_improvement', 'major_purchase', 'medical', 'moving', 'vacation', 'house',
                    'renewable_energy', 'educational'],
    }

    # Crear un DataFrame con todas las categorías
    df_dummies = pd.DataFrame({col: pd.Series(values) for col, values in data_dummies.items()})
    original_columns = pd.get_dummies(df_dummies, drop_first=False)

    # Obtener las columnas en un DataFrame de todas las posibles combinaciones de categorías
    all_columns = list(original_columns.columns)

    print(all_columns)


    # Escalar las columnas numéricas
    final_columns = ['loan_amnt', 'int_rate', 'annual_inc', 'open_acc',
       'revol_bal', 'total_acc', 'out_prncp', 'total_pymnt', 'total_rec_int',
       'last_pymnt_amnt', 'tot_cur_bal', 'total_rev_hi_lim', 'grade_A',
       'grade_B', 'grade_C', 'grade_D', 'grade_E', 'grade_F', 'grade_G',
       'home_ownership_MORTGAGE', 'home_ownership_NONE',
       'home_ownership_OTHER', 'home_ownership_OWN', 'home_ownership_RENT',
       'purpose_car', 'purpose_credit_card', 'purpose_debt_consolidation',
       'purpose_educational', 'purpose_home_improvement', 'purpose_house',
       'purpose_major_purchase', 'purpose_medical', 'purpose_moving',
       'purpose_other', 'purpose_renewable_energy', 'purpose_small_business',
       'purpose_vacation', 'purpose_wedding']

    num_columns = ['loan_amnt', 'int_rate', 'annual_inc', 'open_acc', 'revol_bal',
       'total_acc', 'out_prncp', 'total_pymnt', 'total_rec_int',
       'last_pymnt_amnt', 'tot_cur_bal', 'total_rev_hi_lim']

    data[num_columns] = scaler.transform(data[num_columns])
    print(data)
    data = data.reindex(columns=final_columns, fill_value=0)
    data = data.astype(float)

    data = np.array(data)
    print(data)
    respuesta = int(modelo.predict(data)[0][0] * 100)

    return respuesta

# Título de la app
st.title("Obtenga su puntaje crediticio")

# Crear formulario en Streamlit
with st.form("input_form"):
    loan_amnt = st.number_input("Monto listado del préstamo solicitado por el prestatario.")
    int_rate = st.number_input("Tasa de interés del préstamo.")
    grade = st.selectbox("Calificación asignada al préstamo por LC.", ['B', 'C', 'A', 'E', 'F', 'D', 'G'])
    home_ownership = st.selectbox("Estado de propiedad de vivienda", ['RENT', 'OWN', 'MORTGAGE', 'OTHER', 'NONE', 'ANY'])
    annual_inc = st.number_input("El ingreso anual", min_value=0.0)
    purpose = st.selectbox("Proposito del prestamo", ['credit_card', 'car', 'small_business', 'other', 'wedding', 'debt_consolidation',
                                      'home_improvement', 'major_purchase', 'medical', 'moving', 'vacation', 'house',
                                      'renewable_energy', 'educational'])
    open_acc = st.number_input("Número de líneas de crédito abiertas en el historial de crédito del prestatario")
    revol_bal = st.number_input("Saldo total de crédito rotativo")
    total_acc = st.number_input("Número total de líneas de crédito actualmente en el historial crediticio del prestatario", min_value=0.0)
    out_prncp = st.number_input("Principal pendiente restante para el monto total financiado", min_value=0.0)
    total_pymnt = st.number_input("Pagos recibidos hasta la fecha para el monto total financiado", min_value=0.0)
    total_rec_int = st.number_input("Intereses recibidos hasta la fecha", min_value=0.0)
    last_pymnt_amnt = st.number_input("Último monto total del pago recibido.", min_value=0.0)
    tot_cur_bal = st.number_input("Saldo total actual de todas las cuentas", min_value=0.0)
    total_rev_hi_lim = st.number_input("Límite de crédito total en líneas de crédito rotativas.", min_value=0.0)

    # Botón para enviar el formulario
    submit_button = st.form_submit_button("Preprocesar y mostrar datos")

# Si el formulario fue enviado
if submit_button:
    # Crear un DataFrame con los datos ingresados
    input_data = {
        'loan_amnt': [loan_amnt],
        'int_rate': [int_rate],
        'grade': [grade],
        'home_ownership': [home_ownership],
        'annual_inc': [annual_inc],
        'purpose': [purpose],
        'open_acc': [open_acc],
        'revol_bal': [revol_bal],
        'total_acc': [total_acc],
        'out_prncp': [out_prncp],
        'total_pymnt': [total_pymnt],
        'total_rec_int': [total_rec_int],
        'last_pymnt_amnt': [last_pymnt_amnt],
        'tot_cur_bal': [tot_cur_bal],
        'total_rev_hi_lim': [total_rev_hi_lim],
    }

    # Convertir a DataFrame
    input_df = pd.DataFrame(input_data)

    # Preprocesar los datos
    resultado = preprocess_data(input_df)

    st.write("Datos Preprocesados")
    old_min = 0
    max_val = 850
    min_val = 300
    old_max = 100

    resultado_txt = (resultado - old_min) * (max_val - min_val) / (old_max - old_min) + min_val
    fig = create_gauge(resultado, int(resultado_txt))
    st.pyplot(fig)
