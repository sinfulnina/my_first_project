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
        min_value=0.0, max_value=1.0, value=0.6, step=0.05,
        help="Controls Randomness: Lowering results in less random completions. As the temperature approaches zero, the model will become detministic and repetitive.")

    frequency_penalty = st.slider(
        label='Frequency Penalty',
        min_value=-2.0, max_value=2.0, value=0.0, step=0.1,
        help="How much to penalize new tokens based on their existing frequency in the test so far. Decreases the model's likelihood to repeat the same line verbatim.")

    presence_penalty = st.slider(
        label='Presence Penalty',
        min_value=-2.0, max_value=2.0, value=0.0, step=0.1,
        help="Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.")

    max_tokens = st.slider(
        label='Maximum Token',
        min_value=0, max_value=2000, value=50, step=50,
        help="The maximum number of tokens to generate. This does not tell the AI how long a text it should write, but how many tokens are generated, thus credited for.")

    # SESSION STATES DEFINED

    # SESSION STATES TAB 1 - Sinful Generator
    if 'input_text' not in st.session_state:
        st.session_state['input_text'] = ''

    if 'output_text' not in st.session_state:
        st.session_state['output_text'] = ''

    # SESSION STATES TAB 2 - OpenAI Generator
    if 'input_text2' not in st.session_state:
        st.session_state['input_text2'] = ''

    if 'output_text2' not in st.session_state:
        st.session_state['output_text2'] = ''

    # SESSION STATES TAB 3 - Product Description Generator
    if 'input_text_product_name' not in st.session_state:
        st.session_state['input_text_product_name'] = ''

    if 'input_text_descriptors' not in st.session_state:
        st.session_state['input_text_descriptors'] = ''

    if 'output_text3' not in st.session_state:
        st.session_state['output_text3'] = ''

    # SESSION STATES TAB 4 - SEO Text Generator
    if 'input_text_product_page' not in st.session_state:
        st.session_state['input_text_product_page'] = ''

    if 'input_text_section1' not in st.session_state:
        st.session_state['input_text_section1'] = ''

    if 'input_text_section2' not in st.session_state:
        st.session_state['input_text_section2'] = ''

    if 'input_text_section3' not in st.session_state:
        st.session_state['input_text_section3'] = ''

    if 'output_text4' not in st.session_state:
        st.session_state['output_text4'] = ''

    # SESSION STATES TAB 4 - SEO Text Generator
    if 'input_text_product_page2' not in st.session_state:
        st.session_state['input_text_product_page2'] = ''

    if 'input_text_section11' not in st.session_state:
        st.session_state['input_text_section11'] = ''

    if 'input_text_section22' not in st.session_state:
        st.session_state['input_text_section22'] = ''

    if 'input_text_section33' not in st.session_state:
        st.session_state['input_text_section33'] = ''

    if 'output_text5' not in st.session_state:
        st.session_state['output_text5'] = ''

    if 'output_text6' not in st.session_state:
        st.session_state['output_text6'] = ''

    if 'output_text7' not in st.session_state:
        st.session_state['output_text7'] = ''

    # SESSION STATES TAB 5 - Proofreading
    if 'input_text3' not in st.session_state:
        st.session_state['input_text3'] = ''

    if 'input_text4' not in st.session_state:
        st.session_state['input_text4'] = ''

    if 'output_text8' not in st.session_state:
        st.session_state['output_text8'] = ''

# TAB BAR
tabs_titles = ["Sinful", "OpenAI", "Product Description", "SEO Text", "SEO Text 2", "Proofreading"]

tabs = st.tabs(tabs_titles)

# TAB 1 - Sinful Generator
with tabs[0]:

    container = st.container()
    container.write(emoji.emojize(
        ":exclamation:") + "**The finetuned Sinful text generator is not yet optimal as it has yet to be fed enough text examples.**" + emoji.emojize(
        ":exclamation:"))

    st.header("Sinful Text Generator")
    prompt = st.text_area("What do you want to write about? " + emoji.emojize(":writing_hand:"), key='input_text',
                          help="This text generator is using the Sinful finetuned version of the Davinci engine")

    if st.button('Submit', key='submit'):
        if prompt:
            response = openai.Completion.create(model="davinci:ft-sinful-2022-08-05-08-56-21",
                                                # engine="text-davinci-002",
                                                temperature=temperature,
                                                frequency_penalty=frequency_penalty,
                                                presence_penalty=presence_penalty,
                                                prompt=prompt,
                                                max_tokens=max_tokens,
                                                # stop=["#"]
                                                )
            st.session_state['output_text'] = response['choices'][0]['text']
    st.text_area(label="Output", value=st.session_state['output_text'], height=300, key="output1")

    #st.download_button(
    #    'Download Prompt and Output',
    #    ("PROMPT:\n\n" + prompt + "\n\nOUTPUT:" + st.session_state['output_text']),
    #    "sinful_text_generator.txt",
    #    key="sinful_text_download"
    #)

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Prompt Token Length", value=len(nltk.word_tokenize(st.session_state.input_text)))
    col2.metric(label="Output Token Length", value=len(nltk.word_tokenize(st.session_state.output_text)))
    col3.metric(label="Max Output Token Length", value=2018 - len(nltk.word_tokenize(st.session_state.input_text)))

# TAB 2 - OpenAI Generator
with tabs[1]:
    st.header("OpenAI Text Generator")
    prompt = st.text_area("What do you want to write about? " + emoji.emojize(":writing_hand:"), key='input_text2',
                          help="This text generator is using the non-finetuned version of the Davinci engine", placeholder="E.g Write an outline for a blog post about BDSM")

    if st.button('Submit', key='submit2'):
        if prompt:
            response = openai.Completion.create(# model="davinci:ft-sinful-2022-08-05-08-56-21",
                engine="text-davinci-002",
                temperature=temperature,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                prompt=prompt,
                max_tokens=max_tokens,
                #stop=["#"]
            )
            st.session_state['output_text2'] = response['choices'][0]['text']
    st.text_area(label="Output",value=st.session_state['output_text2'], height=300, key="output2")

    #st.download_button(
    #    'Download Prompt and Output',
    #    ("PROMPT:\n\n" + prompt + "\n\nOUTPUT:" + st.session_state['output_text2']),
    #    "openai_text_generator.txt",
    #    key="openai_text_download"
    #)

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Prompt Token Length", value=len(nltk.word_tokenize(st.session_state.input_text2)))
    col2.metric(label="Output Token Length", value=len(nltk.word_tokenize(st.session_state.output_text2)))
    col3.metric(label="Max Output Token Length", value=2018 - len(nltk.word_tokenize(st.session_state.input_text2)))

# TAB 3 - Product Description Generator
with tabs[2]:
    st.header("Product Description Generator")

    product_name = st.text_input("Product Name", key='input_text_product_name',
                                 placeholder="E.g Satisfyer Pro 2 Next Generation Clitoral Stimulator", help="This text generator is using the non-finetuned version of the Davinci engine")
    descriptions = st.text_input("Product Descriptors " + emoji.emojize(":star-struck:"), key='input_text_descriptors',
                                 placeholder="E.g Bestseller, sleek design, rechargeable, designer, new technologies..")
    tone_of_voice = st.selectbox("Tone of Voice " + emoji.emojize(":speaking_head:"),
                                 ('Excited', 'Professional', 'Encouraging', 'Funny', 'Witty', 'Engaging', 'Creative'),
                                 key='input_tone_of_voice')
    desired_length = st.slider("Desired Length", 0, 500, 200, 25, key="input_desired_length",
                               help="Please remember to set the 'Maximum Token' length to be equal to Desired Length. It is not possible to tell the AI exactly how much text it should generate, though we can prompt a general length using this field.")

    prompt = (
            "Write a creative product description for a product page using the following Name, Descriptors, Tone of Voice and Desired Length." +
            "\n\nNAME: " + product_name +
            "\n\nDESCRIPTORS: " + descriptions +
            "\n\nTONE OF VOICE: " + tone_of_voice +
            "\n\nDESIRED LENGTH: " + str(desired_length) + " words" +
            "\n\nPRODUCT DESCRIPTION:")

    if st.button('Submit', key='submit3'):
        if prompt:
            response = openai.Completion.create(model="davinci:ft-sinful-2022-08-05-08-56-21",
                                                # engine="text-davinci-002",
                                                temperature=temperature,
                                                frequency_penalty=frequency_penalty,
                                                presence_penalty=presence_penalty,
                                                prompt=prompt,
                                                max_tokens=max_tokens
                                                )
            st.session_state['output_text3'] = response['choices'][0]['text']
    st.text_area(label="Output", value=st.session_state['output_text3'], height=300, key="output3")

    #st.download_button(
    #    'Download Prompt and Output',
    #    ("PROMPT:" +
    #     "\n\nProduct Name: " + product_name +
    #     "\n\nProduct Descriptors: " + descriptions +
    #     "\n\nTone of Voice: " + tone_of_voice +
    #     "\n\nDesired Length: " + str(desired_length) + " words" +
    #     "\n\nOUTPUT:\n\nProduct Description" + st.session_state[
    #         'output_text3']),
    #    "product_description_generator.txt",
    #    key="product_description_download"
    #)

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Prompt Token Length", value=len(nltk.word_tokenize(st.session_state.input_text_product_name)) + len(nltk.word_tokenize(st.session_state.input_text_descriptors)) + len(nltk.word_tokenize("Write a creative product description for a product page using the following Name, Descriptors, Tone of Voice and Desired Length. NAME: DESCRIPTORS: TONE OF VOICE: Excited DESIRED LENGTH: 200 words PRODUCT DESCRIPTION:")))
    col2.metric(label="Output Token Length", value=len(nltk.word_tokenize(st.session_state.output_text3)))
    col3.metric(label="Max Output Token Length", value=2018 - (len(nltk.word_tokenize(st.session_state.input_text_product_name)) + len(nltk.word_tokenize(st.session_state.input_text_descriptors)) + len(nltk.word_tokenize("Write a creative product description for a product page using the following Name, Descriptors, Tone of Voice and Desired Length. NAME: DESCRIPTORS: TONE OF VOICE: Excited DESIRED LENGTH: 200 words PRODUCT DESCRIPTION:"))))

# TAB 4 - SEO Text Generator
with tabs[3]:
    st.header("SEO Text Generator")

    product_page = st.text_input("Product Page Name", key='input_text_product_page', placeholder="E.g vibrator", help="This text generator is using the non-finetuned version of the Davinci engine")
    section1 = st.text_input("Heading - Section 1", key='input_text_section1',
                             placeholder="E.g What is a vibrator and how do you use one?").upper()
    section2 = st.text_input("Heading - Section 2", key='input_text_section2',
                             placeholder="E.g Who can use a vibrator and what are the benefits?").upper()
    section3 = st.text_input("Heading - Section 3", key='input_text_section3',
                             placeholder="E.g How to choose the perfect vibrator for you").upper()

    prompt = (
            "Write a Search Engine Optimised text for a " + product_page + " product page with three sections. Use the following three headings as titles for each of the three sections: "
            + "\n\n1. " + section1
            + "\n\n2. " + section2
            + "\n\n3. " + section3
            + ".")

    if st.button('Submit', key='submit4'):
        if prompt:
            response = openai.Completion.create(  # model="davinci:ft-sinful-2022-08-05-08-56-21",
                engine="text-davinci-002",
                temperature=temperature,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                prompt=prompt,
                max_tokens=max_tokens,
                stop=["END"]
            )
            st.session_state['output_text4'] = response['choices'][0]['text']
    st.text_area(label="Output", value=st.session_state['output_text4'], height=300, key="output4")

    #st.download_button(
    #    'Download Prompt and Output',
    #    ("PROMPT:" +
    #     "\n\nProduct Page: " + product_page +
    #     "\n\nHeading - Section 1: " + section1 +
    #     "\n\nHeading - Section 2: " + section2 +
    #     "\n\nHeading - Section 3: " + section3 +
    #     "\n\nOUTPUT:" + st.session_state['output_text4']),
    #    "seo_text_generator.txt",
    #    key="seo_text_download"
    #)

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Prompt Token Length", value=len(nltk.word_tokenize(st.session_state.input_text_product_page)) + len(nltk.word_tokenize(st.session_state.input_text_section1)) + len(nltk.word_tokenize(st.session_state.input_text_section3)) + len(nltk.word_tokenize(st.session_state.input_text_section3)) + len(nltk.word_tokenize("Write a Search Engine Optimised text for a product page with three sections. Use the following three headings as titles for each of the three sections: 1. 2. 3. END")))
    col2.metric(label="Output Token Length", value=len(nltk.word_tokenize(st.session_state.output_text4)))
    col3.metric(label="Max Output Token Length", value=2018 - (len(nltk.word_tokenize(st.session_state.input_text_product_page)) + len(nltk.word_tokenize(st.session_state.input_text_section1)) + len(nltk.word_tokenize(st.session_state.input_text_section3)) + len(nltk.word_tokenize(st.session_state.input_text_section3)) + len(nltk.word_tokenize("Write a Search Engine Optimised text for a product page with three sections. Use the following three headings as titles for each of the three sections: 1. 2. 3. END"))))

# TAB 5 - SEO Text Generator 2

with tabs[4]:
    st.header("SEO Text Generator")

    container = st.container()
    container.write(emoji.emojize(":exclamation:") + "**It is recommended to set the Temperature, Frequency Penalty and Presence Penalty to maximum.**" + emoji.emojize(":exclamation:"))

    product_page = st.text_input("Product Page Name", key='input_text_product_page2', placeholder="E.g vibrator", help="This text generator is using the non-finetuned version of the Davinci engine")

    prompt = ("Write a lengthy, elaborate and creative Search Engine Optimised text for a " + product_page + " sex toy product page. It must explain what a" + product_page + " is, what can a " + product_page + " can be made of, and how to use a " + product_page + ".")
    prompt2 = ("Write a lengthy, elaborate and creative Search Engine Optimised text for a " + product_page + " sex toy product page. It must explain who can use a " + product_page + " and what the benefits of using a " + product_page + " are.")
    prompt3 = ("Write a lengthy, elaborate and creative Search Engine Optimised text for a " + product_page + " sex toy product page. First, describe all the different types of " + product_page + "s, then help explain how someone can choose the right " + product_page + " for them. Throughout, please also mention some specific " + product_page + " products to provide examples.")

    if st.button('Create part 1', key='submit5'):
        if prompt:
            response = openai.Completion.create(
                #model="davinci:ft-sinful-2022-08-05-08-56-21",
                engine="text-davinci-002",
                temperature=temperature,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                prompt=prompt,
                max_tokens=max_tokens,
                stop=["END"]
            )
            st.session_state['output_text5'] = response['choices'][0]['text']
    #st.write(prompt)
    st.text_area(label="Column 1 - What it is, what it is made of and how to use it..", value=st.session_state['output_text5'], height=200, key="output5", placeholder="Press 'Create' once you've entered a product page name")

    if st.button('Create part 2', key='submit6'):
        if prompt2:
            response = openai.Completion.create(
                #model="davinci:ft-sinful-2022-08-05-08-56-21",
                engine="text-davinci-002",
                temperature=temperature,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                prompt=prompt2,
                max_tokens=max_tokens,
                stop=["END"]
            )
            st.session_state['output_text6'] = response['choices'][0]['text']
    #st.write(prompt2)
    st.text_area(label="Column 2 - Who can use it and what are the benefits..", value=st.session_state['output_text6'], height=200, key="output6", placeholder="Press 'Create' once you've entered a product page name")

    if st.button('Create part 3', key='submit7'):
        if prompt3:
            response = openai.Completion.create(
                #model="davinci:ft-sinful-2022-08-05-08-56-21",
                engine="text-davinci-002",
                temperature=temperature,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                prompt=prompt3,
                max_tokens=max_tokens,
                stop=["END"]
            )
            st.session_state['output_text7'] = response['choices'][0]['text']
    #st.write(prompt3)
    st.text_area(label="Column 3 - Describe the different types and how to choose the right one..", value=st.session_state['output_text7'], height=200, key="output7", placeholder="Press 'Create' once you've entered a product page name")

    #st.download_button(
    #    'Download Prompt and Output',
    #    ("PROMPT:" +
    #     "\n\nProduct Page: " + product_page +
    #     "\n\nHeading - Section 1: " + section1 +
    #     "\n\nHeading - Section 2: " + section2 +
    #     "\n\nHeading - Section 3: " + section3 +
    #     "\n\nOUTPUT:" + st.sessaion_state['output_text4']),
    #    "seo_text_generator.txt",
    #    key="seo_text_download"
    #)

    col1, col2 = st.columns(2)
    col1.metric(label="Prompt Token Length", value=(11*len(nltk.word_tokenize(st.session_state.input_text_product_page2))) + len(nltk.word_tokenize(prompt)) + len(nltk.word_tokenize(prompt2)) + len(nltk.word_tokenize(prompt3)))
    col2.metric(label="Output Token Length", value=len(nltk.word_tokenize(st.session_state.output_text5)) + len(nltk.word_tokenize(st.session_state.output_text6)) + len(nltk.word_tokenize(st.session_state.output_text7)))

with tabs[5]:
    st.header("Proofreading")
    proofreading_input = st.text_area("What do you want to have corrected? " + emoji.emojize(":eyes:"), key='input_text3',
                          help="This text generator is using the non-finetuned version of the Davinci engine",
                          placeholder="Insert the text that you want to have corrected")
    instruction = st.text_area("How do you want to correct the text?" + emoji.emojize(":crystal_ball:"), key='input_text4',
                          placeholder="E.g Correct the spelling and grammar", height=10)

    if st.button('Correct', key='submit8'):
        if proofreading_input:
            response = openai.Edit.create(
                model="text-davinci-edit-001",
                temperature=temperature,
                input=proofreading_input,
                instruction=instruction
            )
            st.session_state['output_text8'] = response['choices'][0]['text']
    st.text_area(label="Corrected output", value=st.session_state['output_text8'], height=300, key="output8")

    # st.download_button(
    #    'Download Prompt and Output',
    #    ("PROMPT:\n\n" + prompt + "\n\nOUTPUT:" + st.session_state['output_text2']),
    #    "openai_text_generator.txt",
    #    key="openai_text_download"
    # )

    col1, col2 = st.columns(2)
    col1.metric(label="Prompt Token Length", value=len(nltk.word_tokenize(st.session_state.input_text3)) + len(nltk.word_tokenize(st.session_state.input_text4)))
    col2.metric(label="Output Token Length", value=len(nltk.word_tokenize(st.session_state.output_text8)))

# st.header("Examples")
