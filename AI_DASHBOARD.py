import streamlit as st
import pandas as pd
from openai import OpenAI
import os
import matplotlib.pyplot as plt

# Initialize OpenAI client with API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit page configuration
st.set_page_config(page_title="AI Dashboard Assistant", page_icon=":bar_chart:", layout="wide")

st.markdown(
    "<style>.big-font {font-size:32px; color:#4CAF50;}</style><div class='big-font'>AI Dashboard Assistant</div>",
    unsafe_allow_html=True
)

st.write("Upload your Excel file to get started!")
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file is None:
    st.info("Please upload an Excel file to get started.")
else:
    # Read the Excel file into a DataFrame
    df = pd.read_excel(uploaded_file)
    
    # Display the DataFrame in the app
    st.write("Here is the data from your Excel file:")
    st.dataframe(df)
    # Interactive product filter
    if "Product" in df.columns:
        product = st.selectbox("Choose a product", df["Product"].unique())
        st.write(df[df["Product"] == product])
    else:
        st.warning("Column 'Product' not found in data.")
    
    # Bar chart by Region and Sales if those columns exist
    if "Region" in df.columns and "Sales" in df.columns:
        st.bar_chart(df.groupby("Region")["Sales"].sum())
    else:
        st.warning("Columns 'Region' and/or 'Sales' not found for bar chart.")
    
    # Plot Sales over Date if those columns exist
    if "Date" in df.columns and "Sales" in df.columns:
        fig, ax = plt.subplots()
        ax.plot(df["Date"], df["Sales"])
        ax.set_xlabel("Date")
        ax.set_ylabel("Sales")
        ax.set_title("Sales Over Time")
        st.pyplot(fig)
    else:
        st.warning("Columns 'Date' and/or 'Sales' not found for line plot.")
    
    # Metrics display
    st.metric("Total Rows", len(df))
    
    # Text input for openAI questions
    question = st.text_input("Ask a question about your data:")
    
    if question:
        # Use OpenAI GPT model for a chat completion
        prompt = f"Answer this: {question}"
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[{"role": "user", "content": prompt}],
        )
        answer = response.choices[0].message.content
        st.write(answer)
        
        # Generate Python code via OpenAI model, optionally
        prompt_code = f"Given this dataframe:\n{df.head().to_string()}\nWrite Python code to {question}. Only output code."
        response_code = client.completions.create(
            model="text-davinci-003",
            prompt=prompt_code,
            temperature=0,
            max_tokens=150
        )
        generated_code = response_code.choices[0].text.strip()
        st.code(generated_code)
