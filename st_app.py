import streamlit as st
import pyperclip
import openai
import nltk
import os
nltk.download('punkt')

openai.api_key = st.secrets["OPENAI_API_KEY"]

with st.sidebar:

    st.image(image='https://www.sinful.dk/skin/frontend/sinful/sinful2020/images/logo_black.svg', width=100)

    temperature = st.slider(
        label='Temperature',
        min_value=0.0, max_value=1.0, value=0.6, step=0.1, help="Controls Randomness: Lowering results in less random completions. As the temperature approaches zero, the model will become detministic and repetitive.")

    frequency_penalty = st.slider(
        label='Frequency Penalty',
        min_value=-2.0, max_value=2.0, value=0.0, step=0.1, help="How much to penalize new tokens based on their existing frequency in the test so far. Decreases the model's likelihood to repeat the same line verbatim.")

    max_tokens = st.slider(
        label='Maximum Tokens',
        min_value=0, max_value=2000, value=50, step=50, help="The maximum number of tokens to generate. This does not tell the AI how long a text it should write, but how many tokens are generated, thus credited for.")

    if 'input_text' not in st.session_state:
        st.session_state['input_text'] = ''

    if 'output_text' not in st.session_state:
        st.session_state['output_text'] = ''

    st.metric(label="Prompt Token Length", value=len(nltk.word_tokenize(st.session_state.input_text)))

    st.metric(label="Output Token Length", value=len(nltk.word_tokenize(st.session_state.output_text)))

    st.metric(label="Max Output Token Length", value=2018-len(nltk.word_tokenize(st.session_state.input_text)))

st.header("SEO AI Text Generator")
prompt = st.text_area("What do you want to write about?", key='input_text')

if st.button('Submit'):
    if prompt:
        response = openai.Completion.create(model="davinci:ft-sinful-2022-08-05-08-56-21",
                                            #engine="text-davinci-001",
                                            temperature=temperature,
                                            frequency_penalty=frequency_penalty,
                                            prompt=prompt,
                                            max_tokens=max_tokens,
                                            stop=["#", ":"]
                                            )
        st.session_state['output_text'] = response['choices'][0]['text']
st.write(st.session_state['output_text'])

if st.button('Copy to Clipboard'):
    pyperclip.copy(st.session_state['output_text'])
