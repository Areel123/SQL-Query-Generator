import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv  # Import the dotenv module

# Load the .env file where your API key is stored
load_dotenv()

# Fetch the API key from the .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

def main():
    st.set_page_config(page_title="SQL Query Generator")
    st.markdown(
        """
            <div style="text-align: center;">
                <h1>SQL Query Generator</h1>
                <h3>Hey I can generate SQL Query for you!</h3>
                <p>This tool is a straightforward solution that allows you to generate SQL queries based on your data.</p>
            </div>
        """,
        unsafe_allow_html=True,
    )

    text_input = st.text_area("Enter your prompt here to get SQL query:")

    submit = st.button("Generate SQL Query")
    if submit:
        with st.spinner("Generate SQL Query..."):
            template="""
                Create a SQL Query snippet using the below text:

                ```
                   {text_input}
                ```
                I just want a SQL Query.

            """

            formatted_template=template.format(text_input=text_input)

            response=model.generate_content(formatted_template)
            sql_query=response.text

            sql_query = sql_query.strip().lstrip("```sql").rstrip("```")

            
            expected_output="""
                What would be the expected response of this SQL query snippet:

                     ```
                     {sql_query}
                     ```
                Provide sample tabular Response with no explanation:
                 
             """
            
            expected_output_formatted=expected_output.format(sql_query=sql_query)
            eoutput=model.generate_content(expected_output_formatted)
            eoutput=eoutput.text

            
            explanation="""
                Explain this Sql Query:

                     ```
                     {sql_query}
                     ```
                Please provide with simplest of explanations :
                 
             """

            explanation_formatted=explanation.format(sql_query=sql_query)
            explanation=model.generate_content(explanation_formatted)
            explanation=explanation.text

            with st.container():
                st.success("SQL Query Generated Successfully! Here is your Query Below:")
                st.code(sql_query, language="sql")

                st.success("Expected Output of this SQL Query will be:")
                st.markdown(eoutput)

                st.success("Explanation of this SQL Query:")
                st.markdown(explanation)


if __name__ == "__main__":
    main()