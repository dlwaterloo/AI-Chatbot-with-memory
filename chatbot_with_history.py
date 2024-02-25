import utils
import streamlit as st

from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

st.set_page_config(page_title="Context aware chatbot", page_icon="⭐")
st.header('Context aware chatbot')

class ContextChatbot:

    def __init__(self):
        utils.configure_openai_api_key()
        self.openai_model = "gpt-4-turbo-preview"
        if 'conversation_chain' not in st.session_state:
            st.session_state['conversation_chain'] = self.setup_chain()
    
    def setup_chain(self):
        memory = ConversationBufferMemory()
        llm = OpenAI(model_name=self.openai_model, temperature=0, streaming=False)
        chain = ConversationChain(llm=llm, memory=memory, verbose=True)
        return chain
    
    @utils.enable_chat_history
    def main(self):
        chain = st.session_state['conversation_chain']
        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            utils.display_msg(user_query, 'user')
            response = chain.run(user_query)
            utils.display_msg(response, 'assistant')
                

if __name__ == "__main__":
    obj = ContextChatbot()
    obj.main()