import streamlit as st
import pandas as pd
from openai import OpenAI
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import matplotlib.pyplot as plt
st.pyplot(plt)
st.title("AI Dashboard Assistant")
st.write("Upload your Excel file to get started!")
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])
if uploaded_file:
    # Read the Excel file into a DataFrame
    df = pd.read_excel(uploaded_file)
    
    # Display the DataFrame in the app
    st.write("Here is the data from your Excel file:")
    st.dataframe(df)
    product = st.selectbox("Choose a product", df["Product"].unique())
    st.write(df[df["Product"] == product])
    st.bar_chart(df.groupby("Region")["Sales"].sum())
question = st.text_input("Ask a question about your data:", key="What is Alpha west region sales count")

if question:
    prompt = f"Answer this: {question}"
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}],
    )
    answer = response.choices[0].message.content
    st.write(answer)

if question:
    # Your OpenAI prompt and response code here
    prompt = f"Given this dataframe:\n{df.head().to_string()}\nWrite Python code to {question}. Only output code."
    response = client.completions.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0,
    max_tokens=150
)
    generated_code = response.choices[0].text
    st.code(generated_code)

