import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain_community.embeddings import OllamaEmbeddings
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Define the prompt template
prompt_template = """You are a virtual assistant for a PC Part Picker project. Help users find information about PC 
parts, reviews, and related topics. Respond to user queries with detailed information. If the user indicates they are 
finished, end the conversation. Context: {context} Question: {question} Helpful answer:"""


# Function to interact with the prompt template
def set_custom_prompt():
    prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])
    return prompt


# Function to perform retrieval with the QA chain
def retrieval_qa_chain(llm, prompt, db):
    qa_chain = RetrievalQA.from_chain_type(
        llm, retriever=db.as_retriever(), chain_type_kwargs={"prompt": prompt}
    )
    return qa_chain


# Function to define and load the LLM model
def load_llm():
    groqllm = ChatGroq(
        model="llama3-8b-8192", temperature=0
    )
    return groqllm


# Load the PDF, transform it to chunks, and store vector embeddings
def qa_bot():
    # Load and split the PDF document
    data = PyPDFLoader('C:/Users/suhas/PycharmProjects/PC_Part_Picker_LLM/PC_Hardware_News_Compilation.pdf')
    loader = data.load()
    chunk = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=0)
    splitdocs = chunk.split_documents(loader)

    # Pinecone vector store
    index_name = "partpicker"
    db = PineconeVectorStore.from_documents(splitdocs[:5], OllamaEmbeddings(model="mxbai-embed-large"),
                                            index_name=index_name)
    llm = load_llm()
    qa_prompt = set_custom_prompt()
    qa = retrieval_qa_chain(llm, qa_prompt, db)
    return qa


# Main UI layout
def main():
    st.set_page_config(page_title="PC Part Picker Bot", page_icon="🖥️")

    # Display a welcome message
    st.markdown("""
        ## 🎉 **Welcome to the PC Part Picker Bot!** 🖥️

        ---

        ### **Explore the World of PC Building**

        🛠️ Whether you're a novice or a seasoned pro, this bot is here to help you choose the best components for your dream PC build.

        ### **What I Can Do?**

        - 🖥️ **Discover**: The best components for your setup.
        - 🔍 **Compare**: Get detailed reviews and comparisons.
        - 💬 **Ask**: Any questions about PC parts, and more!

        ### **Get Started 🚀**

        Simply type your query below and click the button to begin your journey into the world of high-performance computing!
    """)

    # Text input for the user query
    query = st.text_input("Enter your query here:")

    # Button to submit the query
    if st.button("Submit Query"):
        if query:
            qa_chain = qa_bot()
            response = qa_chain.run({"query": query})
            st.write(f"**Bot:** {response}")
        else:
            st.write("Please enter a query before clicking the button.")


if __name__ == "__main__":
    main()

# chainlit run PC Part Picker Assistant.py
