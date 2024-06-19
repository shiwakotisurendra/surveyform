import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(layout='wide')
st.title("Geoinformation feedback Portal")

# SQLite DB Setup
conn = sqlite3.connect('geoinformation_feedback.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
          CREATE TABLE IF NOT EXISTS population
          ([name] TEXT, [address] TEXT, [answer] TEXT, [address2] TEXT, 
          [answer2] TEXT, [address3] TEXT, [answer3] TEXT, [address4] TEXT, 
          [answer4] TEXT, [address5] TEXT, [answer5] TEXT, [qualification] TEXT, 
          [country] TEXT, [population] INTEGER, [age] INTEGER, [additional] TEXT)
          ''')

# Function to read existing data from the SQLite database
def read_data(conn):
    df = pd.read_sql_query("SELECT * FROM population", conn)
    return df.dropna(how='all')  # Drop rows where all elements are missing.

existing_data = read_data(conn)
# btn1= st.button("Download *.CSV")
# if btn1:
# st.download_button('Download',existing_data.to_csv(),'data.csv')
# st.dataframe(existing_data)

# Questions and options setup
address1 = ["A,B,C"]
qualification1 = ['1','2','3']
a= st.chat_input()

# Onboarding New Vendor Form
with st.form(key="vendor_form"):
    st.subheader("Department*")
    name = st.text_input(label="answer:")
    # Assemble questions and input fields
    address = st.subheader("Q1. Welche Fachbereiche der Stadt Kerpen könnten von dem InfoTool zur Klimaanpassung profitieren und dieses auch nutzen?")#st.selectbox("question1*", options=address1, index=None)
    answer= st.radio('answer1:',['A','B','C'])#st.text_area(label="answer1")
    address2 = st.subheader("Q2. Welche Abteilung soll der Ansprechpartner für das InfoTool zur Klimaanpassung sein?")#st.selectbox("question2*", options=address1, index=None)
    answer2= st.text_area(label="answer2 :")
    address3 = st.subheader("Q3. Sollte das InfoTool auch für andere Nutzer/Städtepartner zur Verfügung stehen, z.B. Wasser-/Umweltverbände, Bürgerinitiativen, Universitäten und Schulen?") #st.selectbox("question3*", options=address1, index=None)
    answer3= st.text_area(label="answer3 :")
    address4 = st.subheader("Q4.  Was sind Ihrer Meinung nach die größten Herausforderungen/Gefahren in Bezug auf den Klimawandel für die Stadt Kerpen?") #st.selectbox("question4*", options=address1, index=None)
    answer4= st.text_area(label="answer4 :")
    address5 = st.subheader("Q5. Welche sind Ihrer Meinung nach die wichtigsten Sektoren, die sich in der Stadt Kerpen mit Klimaanpassung befassen, z.B. Klima-/Umweltabteilungen, Stadtplaner, Wasserwirtschaft, Landwirtschaft, Bergbau, Industrie, Rettungsdienste, usw. ?")#st.selectbox("question5*", options=address1, index=None)
    answer5= st.text_area(label="answer5 :")
    st.subheader("Products Offered")
    qualification = st.radio("answer6:",options=qualification1)
    st.subheader("Region/City")
    country = st.text_input(label="answer7 :") 
    st.subheader("Population")
    population = st.number_input(label="answer8 :",min_value=0)
    st.subheader("Years in Business")
    age = st.slider("answer9 :", 0, 50, 5)
    st.subheader("Additional Notes")
    additional_info = st.text_area(label="answer10 :")

    # Mark mandatory fields
    st.markdown("**required*")
    submit_button = st.form_submit_button(label="Submit Survey Details")

    # If the submit button is pressed
    if submit_button:
        if not name:
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()
        elif existing_data['name'].astype(str).str.contains(name).any():
            st.warning("A department with this name already exists.")
            st.stop()
        else:
            # Prepare the vendor data for insertion
            vendor_data = (name, answer, answer2, answer3, answer4, answer5,
                           ", ".join(qualification), country, population, age, additional_info)

            # Insert new vendor into the SQLite database
            c.execute('''
                      INSERT INTO population (name, answer, answer2, answer3, answer4, answer5, 
                      qualification, country, population, age, additional)
                      VALUES (?,?,?,?,?,?,?,?,?,?,?)
                      ''', (vendor_data))
            conn.commit()

            st.success("Survey details successfully submitted!")
            st.balloons()
            # Refresh and display the updated DataFrame
            # updated_df = read_data(conn)
            # st.dataframe(updated_df)
