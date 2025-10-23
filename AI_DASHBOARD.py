import streamlit as st
import pandas as pd
from openai import OpenAI
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import matplotlib.pyplot as plt

st.title("AI Dashboard Assistant")
st.write("Upload your Excel file to get started!")
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])
if uploaded_file is None:
    st.info("Please upload an Excel file to get started.")
else:
    st.write("File uploaded successfully!")   # Debugging line
    # add more lines to print the DataFrame or keys, e.g.:
   
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
# Create a figure and plot sample data
# Display the plot in Streamlit
fig, ax = plt.subplots()
x_data = df["Date"]
y_data = df["Sales"]
ax.plot(x_data, y_data)
ax.set_xlabel("Date")   # Set x-axis label accordingly
ax.set_ylabel("Sales")  # Set y-axis label accordingly
ax.set_title("Sales Over Time")

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
st.set_page_config(
    page_title="AI Dashboard Assistant",
    page_icon=":bar_chart:",
    layout="wide"
)
col1, col2 = st.columns(2)
with col1:
    st.header("Data Table")
    st.dataframe(df)
with col2:
    st.header("Visualization")
    st.pyplot(fig)
with st.spinner("Processing file..."):
    df = pd.read_excel(uploaded_file)
st.success("File loaded and processed!")
st.metric("Total Rows", len(df))
st.markdown(
    "<style>.big-font {font-size:32px; color:#4CAF50;}</style><div class='big-font'>AI Dashboard Assistant</div>",
    unsafe_allow_html=True
)

