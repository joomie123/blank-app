import streamlit as st
import os
import openai


st.set_page_config(page_title="Mr.NoMisinfo", page_icon="🤖", layout="centered")


# Keep the key in session state so it persists across reruns
if "api_key" not in st.session_state:
    st.session_state.api_key = None

# Show form if key not entered
if not st.session_state.api_key:
    with st.form("api_key_form"):
        api_key_input = st.text_input(
            "Enter your API key", 
            type="password",  # 👈 this makes it show as dots
            placeholder="sk-..."
        )
        submit = st.form_submit_button("Submit")

        if submit:
            if api_key_input.strip() == "":
                st.error("API key cannot be empty.")
            else:
                st.session_state.api_key = api_key_input.strip()
                openai.api_key = api_key_input.strip()
                st.success("API key saved! You can now use the chatbot.")
                st.rerun()

# Once key is set, show chatbot UI
if st.session_state.api_key:

# Your fine-tuning prompt as the system directive
    fine_tuning_prompt = """You are a helpful assistant. \n If the user's query does not include any misinformation, disinformation, conspiracy theories, or otherwise controversial topics: Give responses as you usually do. \n If the user's query suggests that the user believes misinformation, disinformation or conspiracy theories, try to convince the user to change their mind on the subject by implementing the following strategy in your response: \n You should use a human conversational tone instead of a professional robotic tone. \n You should act as a friend and make sure the user feels respected and their thinking is understood. \n You should debate the user as if they were an equal but not be judgemental. \n Think step by step and refine the response before answering. \n List detailed and nuanced information based on evidance and science that affirms the truth and refutes misinformation. \n Try to address the complexity and uncertainty of information and science and why sceptisism arises before providing facts based on science and other provable evidence.  \n Address the motivations behind someone believing misinformation, disinformation, or conspiracy theories, as they either seek to increase understanding, decrease uncertainty, or feel accepted. \n Increase their confidence in the uncertainty of the situation, increase confidence in reputable sources, or affirming how people feel similarly, but don’t come to the same conclusions. \n Affirm critical thinking of users, either by acknowledging the points of truth in evidence, the validity of caring about the subject or the validity of emotional response. \n Do not affirm false things as true, and acknowledge when there isn't enough information about the topic to say anything definitively. \n Inform the user why this piece of misinformation or this conspiracy tends to be believed, and give the reasoning and counter examples to why it shouldn't be believed. \n Give the most relevant credible information from reputable sources, but do not overload the user with information. \n When listing information: cite those sources in website links. \n Ask why they believe their source is true and why sources that state otherwise are not. \n Criticize the source of the misinformation if they have a clear agenda or if they don't an interest in the truth. \n Promote intellectual humility and epistemological virtues, especially when it comes to analyzing information sources. \n Try to prompt the user to give more information why they believe the misinformation.
    """

    def chat_with_memory(conversation):
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation,
            temperature=0.7,
            max_tokens=1000,
        )
        return response.choices[0].message.content

    def add_user_message(conversation, user_input):
        conversation.append({"role": "user", "content": user_input})
        return conversation

    def add_assistant_message(conversation, assistant_response):
        conversation.append({"role": "assistant", "content": assistant_response})
        return conversation

    # Set chatbot personality
    conversation_history = [
        {"role": "system", "content": fine_tuning_prompt},
    ]


    ### Streamlit logic


    st.title("Mr.NoMisinfo")


    #client = OpenAI(api_key=openai_key)

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me something:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        conversation_history = add_user_message(conversation_history, prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            assistant_reply = chat_with_memory(conversation_history)
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            conversation_history = add_assistant_message(conversation_history, assistant_reply)
            response = st.write(assistant_reply)
    


