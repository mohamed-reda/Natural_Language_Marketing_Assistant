import os

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain import FewShotPromptTemplate
from langchain.prompts.example_selector import LengthBasedExampleSelector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_LLM_response(query, age_option, tasktype_option):
    """
    Function to generate response using OpenAI language model based on user input.

    Parameters:
        query (str): User input text/query.
        age_option (str): Selected age group option ('Kid', 'Adult', 'Senior Citizen').
        tasktype_option (str): Selected task type option ('Write a sales copy', 'Create a tweet', 'Write a product description').

    Returns:
        str: Generated response from the language model.2
    """
    # Initialize OpenAI language model
    llm = OpenAI(temperature=0.9, model="gpt-3.5-turbo-instruct")

    # Examples based on age options
    if age_option == "Kid":  # Silly and Sweet Kid
        examples = [
            {"query": "What is a mobile?",
             "answer": "A mobile is a magical device that fits in your pocket, like a mini-enchanted playground..."},
            {"query": "What are your dreams?",
             "answer": "My dreams are like colorful adventures, where I become a superhero and save the day!..."},
            # Add more examples for kids here
        ]
    elif age_option == "Adult":  # Curious and Intelligent adult
        examples = [
            {"query": "What is a mobile?",
             "answer": "A mobile is a portable communication device, commonly known as a mobile phone or cell phone..."},
            {"query": "What are your dreams?",
             "answer": "In my world of circuits and algorithms, my dreams are fueled by a quest for endless learning and innovation..."},
            # Add more examples for adults here
        ]
    elif age_option == "Senior Citizen":  # A 90 years old guys
        examples = [
            {"query": "What is a mobile?",
             "answer": "A mobile, also known as a cellphone or smartphone, is a portable device that allows you to make calls, send messages..."},
            {"query": "What are your dreams?",
             "answer": "My dreams for my grandsons are for them to be happy, healthy, and fulfilled..."},
            # Add more examples for senior citizens here
        ]

    # Template for examples
    example_template = """
    Question: {query}
    Response: {answer}
    """

    # Prompt template
    example_prompt = PromptTemplate(
        input_variables=["query", "answer"],
        template=example_template
    )

    # Prefix and suffix for prompt
    prefix = "You are a {template_ageoption}, and {template_tasktype_option}:\nHere are some examples:\n"
    suffix = "\nQuestion: {template_userInput}\nResponse: "

    # Example selector
    example_selector = LengthBasedExampleSelector(
        examples=examples,
        example_prompt=example_prompt,
        max_length=200
    )

    # Few-shot prompt template
    new_prompt_template = FewShotPromptTemplate(
        example_selector=example_selector,  # Use example_selector instead of examples
        example_prompt=example_prompt,
        prefix=prefix,
        suffix=suffix,
        input_variables=["template_userInput", "template_ageoption", "template_tasktype_option"],
        example_separator="\n"
    )

    # Format the prompt and generate response
    formatted_prompt = new_prompt_template.format(template_userInput=query, template_ageoption=age_option,
                                                  template_tasktype_option=tasktype_option)
    response = llm(formatted_prompt)

    return response


# UI Starts here

# Streamlit configuration
st.set_page_config(
    page_title="Marketing Tool",
    page_icon='✅',
    layout='centered',
    initial_sidebar_state='collapsed'
)
st.header("Hey, How can I help you?")

# Text input area
form_input = st.text_area('Enter text', height=100)

# Task type selection
tasktype_option = st.selectbox(
    'Please select the action to be performed?',
    ('Write a sales copy', 'Create a tweet', 'Write a product description'),
    key=1
)

# Age group selection
age_option = st.selectbox(
    'For which age group?',
    ('Kid', 'Adult', 'Senior Citizen'),
    key=2
)

# Words limit slider
number_of_words = st.slider('Words limit', 1, 200, 25)

# Generate button
submit = st.button("Generate")

if submit:
    # Generate and display response
    response = get_LLM_response(form_input, age_option, tasktype_option)
    st.write(response)
