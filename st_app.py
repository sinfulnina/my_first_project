import streamlit as st
import openai
import nltk
import os
import emoji
nltk.download('punkt')

# EMOJI LINK https://carpedm20.github.io/emoji/

#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = st.secrets["OPENAI_API_KEY"]

with st.sidebar:

    st.image(image='https://www.sinful.dk/skin/frontend/sinful/sinful2020/images/logo_black.svg', width=100)

    temperature = st.slider(
        label='Temperature',
        min_value=0.0, max_value=1.0, value=0.6, step=0.05, help="Controls Randomness: Lowering results in less random completions. As the temperature approaches zero, the model will become detministic and repetitive.")

    frequency_penalty = st.slider(
        label='Frequency Penalty',
        min_value=-2.0, max_value=2.0, value=0.0, step=0.1, help="How much to penalize new tokens based on their existing frequency in the test so far. Decreases the model's likelihood to repeat the same line verbatim.")

    max_tokens = st.slider(
        label='Maximum Token',
        min_value=0, max_value=2000, value=50, step=50, help="The maximum number of tokens to generate. This does not tell the AI how long a text it should write, but how many tokens are generated, thus credited for.")

    if 'input_text' not in st.session_state:
        st.session_state['input_text'] = ''

    if 'input_text2' not in st.session_state:
        st.session_state['input_text2'] = ''

    if 'input_text3' not in st.session_state:
        st.session_state['input_text3'] = ''

    if 'input_text4' not in st.session_state:
        st.session_state['input_text4'] = ''

    if 'output_text' not in st.session_state:
        st.session_state['output_text'] = ''

    if 'output_text2' not in st.session_state:
        st.session_state['output_text2'] = ''

    if 'output_text3' not in st.session_state:
        st.session_state['output_text3'] = ''

    if 'output_text4' not in st.session_state:
        st.session_state['output_text4'] = ''

    st.metric(label="Prompt Token Length", value=len(nltk.word_tokenize(st.session_state.input_text)))

    st.metric(label="Output Token Length", value=len(nltk.word_tokenize(st.session_state.output_text)))

    st.metric(label="Max Output Token Length", value=2018-len(nltk.word_tokenize(st.session_state.input_text)))

tabs_titles = ["Sinful Generator","OpenAI Generator","Product Description Generator","SEO Text Generator"]

tabs = st.tabs(tabs_titles)

with tabs[0]:

    st.header("Sinful Text Generator")
    prompt = st.text_area("What do you want to write about? " + emoji.emojize(":writing_hand:"), key='input_text', help="This text generator is using the Sinful finetuned version of the Davinci engine")

    if st.button('Submit', key='submit'):
        if prompt:
            response = openai.Completion.create(model="davinci:ft-sinful-2022-08-05-08-56-21",
                                                #engine="text-davinci-001",
                                                temperature=temperature,
                                                frequency_penalty=frequency_penalty,
                                                prompt=prompt,
                                                max_tokens=max_tokens,
                                                #stop=["#"]
                                                )
            st.session_state['output_text'] = response['choices'][0]['text']
    st.write(st.session_state['output_text'])

    st.download_button(
        'Download Prompt and Output',
        ("PROMPT:\n\n" + prompt + "\n\nOUTPUT:" + st.session_state['output_text']),
        "sinful_text_generator.txt",
        key="sinful_text_download"
    )

with tabs[1]:
    st.header("OpenAI Text Generator")
    prompt = st.text_area("What do you want to write about? " + emoji.emojize(":writing_hand:"), key='input_text2', help="This text generator is using the non-finetuned version of the Davinci engine")

    if st.button('Submit', key='submit2'):
        if prompt:
            response = openai.Completion.create(#model="davinci:ft-sinful-2022-08-05-08-56-21",
                                                engine="text-davinci-001",
                                                temperature=temperature,
                                                frequency_penalty=frequency_penalty,
                                                prompt=prompt,
                                                max_tokens=max_tokens,
                                                #stop=["#"]
                                                )
            st.session_state['output_text2'] = response['choices'][0]['text']
    st.write(st.session_state['output_text2'])

    st.download_button(
        'Download Prompt and Output',
        ("PROMPT:\n\n" + prompt + "\n\nOUTPUT:" + st.session_state['output_text2']),
        "openai_text_generator.txt",
        key="openai_text_download"
    )

with tabs[2]:
    st.header("Product Description Generator")

    product_name = st.text_input("Product Name", key='input_text_product_name', placeholder="E.g. Satisfyer Pro 2 Next Generation Clitoral Stimulator")
    descriptions = st.text_input("Product Descriptors " + emoji.emojize(":star-struck:"), key='input_text_descriptors', placeholder="E.g Bestseller, sleek design, rechargeable, designer, new technologies..")
    tone_of_voice = st.selectbox("Tone of Voice " + emoji.emojize(":speaking_head:"), ('Excited', 'Professional', 'Encouraging', 'Funny', 'Witty', 'Engaging', 'Creative'), key='input_tone_of_voice')
    desired_length = st.slider("Desired Length",0, 500, 200, 25, help="Please remember to set the 'Maximum Token' length to be equal to Desired Length. It is not possible to tell the AI exactly how much text it should generate, though we can prompt a general length using this field.")

    prompt = ("Write a creative product description for a product page using the following Name, Descriptors, Tone of Voice and Desired Length." +
        "\n\nNAME: " + product_name +
        "\n\nDESCRIPTORS: " + descriptions +
        "\n\nTONE OF VOICE: " + tone_of_voice +
        "\n\nDESIRED LENGTH: " + str(desired_length) + " words" +
        "\n\nPRODUCT DESCRIPTION:")

    st.write(prompt)

    if st.button('Submit', key='submit3'):
        if prompt:
            response = openai.Completion.create(model="davinci:ft-sinful-2022-08-05-08-56-21",
                                                #engine="text-davinci-001",
                                                temperature=temperature,
                                                frequency_penalty=frequency_penalty,
                                                prompt=prompt,
                                                max_tokens=max_tokens,
                                                )
            st.session_state['output_text3'] = response['choices'][0]['text']
    st.write(st.session_state['output_text3'])

    st.download_button(
        'Download Prompt and Output',
        ("PROMPT:" +
         "\n\nProduct Name: " + product_name +
         "\n\nProduct Descriptors: " + descriptions +
         "\n\nTone of Voice: " + tone_of_voice +
         "\n\nDesired Length: " + str(desired_length) + " words"
         "\n\nOUTPUT:\n\nProduct Description" + st.session_state['output_text3']),
        "product_description_generator.txt",
        key="product_description_download"
    )

with tabs[3]:
    st.header("SEO Text Generator")

    product_page = st.text_input("Product Page Name", key='input_text_product_page', placeholder="E.g Vibrator")
    section1 = st.text_input("Heading - Section 1", key='input_text_section1', placeholder="E.g What is a vibrator?").upper()
    section2 = st.text_input("Heading - Section 2", key='input_text_section2', placeholder="E.g Why every women should own a vibrator").upper()
    section3 = st.text_input("Heading - Section 3", key='input_text_section3', placeholder="E.g How to choose the perfect vibrator for you").upper()

    prompt = ("Write a Search Engine Optimised text for a " + product_page + " product page with three sections. Use the following three headings as titles for each of the three sections: "
               + "\n\n1. " + section1
               + "\n\n2. " + section2
               + "\n\n3. " + section3
               + "\n\nEND")

    if st.button('Submit', key='submit4'):
        if prompt:
            response = openai.Completion.create(#model="davinci:ft-sinful-2022-08-05-08-56-21",
                                                engine="text-davinci-001",
                                                temperature=temperature,
                                                frequency_penalty=frequency_penalty,
                                                prompt=prompt,
                                                max_tokens=max_tokens,
                                                stop=["END"]
                                                )
            st.session_state['output_text4'] = response['choices'][0]['text']
    st.write(st.session_state['output_text4'])

    st.download_button(
        'Download Prompt and Output',
        ("PROMPT:" +
         "\n\nProduct Page: " + product_page +
         "\n\nHeading - Section 1: " + section1 +
         "\n\nHeading - Section 2: " + section2 +
         "\n\nHeading - Section 3: " + section3 +
         "\n\nOUTPUT:" + st.session_state['output_text4']),
        "seo_text_generator.txt",
        key="seo_text_download"
    )

#with tabs[4]:

    #st.header("Examples")
