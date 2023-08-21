import streamlit as st
import replicate
import os

# App title
st.set_page_config(page_title="AI Chatbot")

if "auth" not in st.session_state:
    st.session_state["auth"] = False
if "username" not in st.session_state:
    st.session_state['username'] = ''
if (st.session_state.auth):
    # Replicate Credentials
    with st.sidebar:
        st.title('Chatbot')
        if 'REPLICATE_API_TOKEN' in st.secrets:
            replicate_api = st.secrets['REPLICATE_API_TOKEN']
        else:
            st.error("Error in connection")
        st.subheader('Models Available')
        selected_model = st.sidebar.selectbox('Choose a model', ['Llama2-7B', 'Llama2-13B', 'Llama2-70B'], key='selected_model')
        
        #Checkout LLama models at  https://replicate.com/replicate/llama-2-70b-chat
        if selected_model == 'Llama2-7B':
            llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
        elif selected_model == 'Llama2-13B':
            llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
        else:
            llm = 'replicate/llama70b-v2-chat:e951f18578850b652510200860fc4ea62b3b16fac280f83ff32282f87bbd2e48'
        
        logout_button = st.button("Logout")
        if logout_button:
            st.session_state.auth = False
            st.session_state.username = ''
            st.experimental_rerun()
        
    os.environ['REPLICATE_API_TOKEN'] = replicate_api

    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "Hello " + st.session_state.username + " How may I assist you today?"}]

    # Display or clear chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    def clear_chat_history():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    # Function for generating LLaMA2 response
    def generate_llama2_response(prompt_input):
        string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
        for dict_message in st.session_state.messages:
            if dict_message["role"] == "user":
                string_dialogue += "User: " + dict_message["content"] + "\n\n"
            else:
                string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
        output = replicate.run(llm, 
                            input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                    "repetition_penalty":1})
        return output

    # User-provided prompt
    if prompt := st.chat_input(disabled=not replicate_api):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_llama2_response(prompt)
                placeholder = st.empty()
                full_response = ''
                for item in response:
                    full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)
else:
    st.title("Please login/sign up to view this page")
