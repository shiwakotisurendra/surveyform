import streamlit as st
import sqlite3
import pandas as pd
import requests 

st.set_page_config(layout='wide')

# url = "https://github.com/shiwakotisurendra/surveyform/raw/master/geoinformation_feedback.db"
# response = requests.get(url)

# if response.status_code == 200:
#     with open("geoinformation_feedback.db", "wb") as file:
#         file.write(response.content)
#     print("Download completed successfully!")
# else:
#     print(f"Failed to download file. Status code: {response.status_code}")


# SQLite DB Setup
conn = sqlite3.connect('geoinformation_feedback.db')
c = conn.cursor()

# Function to read existing data from the SQLite database
def read_data(conn):
    df = pd.read_sql_query("SELECT rowid,* FROM population", conn)
    return df.dropna(how='all')  # Drop rows where all elements are missing.

# Function to delete a row
def delete_row_by_id(conn, row_id):
    """
    Delete a row from the population table based on the rowid.
    """
    sql = 'DELETE FROM population WHERE rowid = ?'
    cur = conn.cursor()
    cur.execute(sql, (row_id,))
    conn.commit()


df_to_edit = read_data(conn)

st.write("Dataframe:", df_to_edit[df_to_edit.columns[1:]])

# For deletion
st.subheader("Delete a row")
row_to_delete = st.selectbox("Select a row to delete:", pd.Series(df_to_edit['rowid']), key="deletion")

if st.button("Delete Row"):
    if row_to_delete:
        delete_row_by_id(conn, row_to_delete)
        st.success(f"Row {row_to_delete} deleted successfully.")
        # Refresh the displayed data after deletion
        df_to_edit = read_data(conn)
        st.write("Updated Dataframe:", df_to_edit)
    else:
        st.error("Please select a valid row to delete.")


# st.dataframe(df_to_edit)
st.subheader("Edit the data")
row_to_edit = st.selectbox("Select a row to edit:", df_to_edit['rowid'])

# Get the details of the selected row
selected_row = df_to_edit[df_to_edit['rowid'] == row_to_edit]

if not selected_row.empty:
    # Pre-fill form with the current values

    edited_name = st.text_input("Name", value=selected_row.iloc[0]['name'])
    edited_address = st.text_input("Question1", value=selected_row.iloc[0]['address'])
    edited_answer = st.text_input("Answer1", value=selected_row.iloc[0]['answer'])
    edited_population = st.number_input("Population", value=int(selected_row.iloc[0]['population']))

    if st.button('Save Changes'):
        # SQL query to update the row

        update_query = "UPDATE population SET name = ?, address = ?, answer = ?, population = ? WHERE rowid = ?"
        c.execute(update_query, (edited_name, edited_address, edited_answer, edited_population, row_to_edit))
        conn.commit()
        st.success("Updated successfully!")


# st.dataframe(existing_data)
updated_df = read_data(conn)
st.download_button('Download',updated_df.to_csv(),'data.csv')
st.dataframe(updated_df)