import streamlit as st
import pandas as pd
import altair as alt

# Load the data
def load_data():
    return pd.read_csv('supermarkt_sales.csv')  # Altere o nome do arquivo para o seu arquivo CSV

def main():
    # Load the data
    data = load_data()

    # Set the page configuration
    st.markdown(
        f"""
        <style>
            .reportview-container .main .block-container {{
                max-width: 1200px;
                padding-top: 2rem;
                padding-right: 2rem;
                padding-left: 2rem;
                padding-bottom: 3rem;
            }}
            h1 {{
                text-align: center;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title('Dashboard teste')

    # Abas
    aba1, aba2 = st.tabs(["Base de dados", "Gráficos"])

    with aba1:  
        st.dataframe(data)

        # Sidebar filters
        partner_filter = st.sidebar.multiselect('Selecione o Parceiro:', ['Todos os Parceiros'] + list(data['Parceiro'].unique()))
        month_text_filter = st.sidebar.selectbox('Selecione o Mês (texto):', ['Todos os Meses'] + list(data['Mês (text)'].unique()))

        # Filtering the dataframe
        if 'Todos os Parceiros' in partner_filter:
            filtered_df = data[data['Mês (text)'] == month_text_filter]
        elif 'Todos os Meses' in month_text_filter:
            filtered_df = data[data['Parceiro'].isin(partner_filter)]
        else:
            filtered_df = data[(data['Parceiro'].isin(partner_filter)) & (data['Mês (text)'] == month_text_filter)]

        # Display the filtered dataframe with a larger table using st.table
        st.table(filtered_df)

    with aba2:
        st.subheader('Gráficos')

        # Seletor para escolher o tipo de gráfico
        chart_type = st.sidebar.selectbox('Escolha o Tipo de Gráfico:', ['Vendas por Parceiro', 'Qtd de Acessos ao Longo do Tempo'])

        # Vendas por Parceiro
        if chart_type == 'Vendas por Parceiro':
            st.subheader('Vendas por Parceiro')
            sales_chart = alt.Chart(filtered_df).mark_bar().encode(
                x='Parceiro',
                y='N° de vendas'
            ).interactive()
            st.altair_chart(sales_chart, use_container_width=True)

        # Qtd de Acessos ao Longo do Tempo
        elif chart_type == 'Qtd de Acessos ao Longo do Tempo':
            st.subheader('Qtd de Acessos ao Longo do Tempo')
            access_chart = alt.Chart(filtered_df).mark_line().encode(
                x='Data:T',
                y='Qtd de acessos',
                color='Parceiro',
                tooltip=['Parceiro', 'Data', 'Qtd de acessos']
            ).interactive()
            st.altair_chart(access_chart, use_container_width=True)

    # Save the modified data to a CSV file
    filtered_df.to_csv('sales_data_filtered.csv', index=False)

if __name__ == '__main__':
    main()
