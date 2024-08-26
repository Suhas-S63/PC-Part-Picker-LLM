import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain.embeddings import OllamaEmbeddings
import chainlit as cl
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
    data = PyPDFLoader('C:/Users/suhas/PycharmProjects/PC Part Picker LLM/PC_Hardware_News_Compilation.pdf')
    loader = data.load()
    chunk = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=0)
    splitdocs = chunk.split_documents(loader)

    # Create the Pinecone vector store
    index_name = "pcpartsnews"
    db = PineconeVectorStore.from_documents(splitdocs[:5], OllamaEmbeddings(model="mxbai-embed-large"),
                                            index_name=index_name)
    llm = load_llm()
    qa_prompt = set_custom_prompt()
    qa = retrieval_qa_chain(llm, qa_prompt, db)
    return qa


# Chainlit decorator for starting the app
@cl.on_chat_start
async def start():
    chain = qa_bot()
    msg = cl.Message(content="Starting the bot...")
    await msg.send()
    msg.content = ("Hi, Welcome to the PC Part Picker Bot. What can I help you with today? You can ask about PC "
                   "parts, reviews, or related topics.")
    await msg.update()

    cl.user_session.set("chain", chain)


# Main functionality to handle user messages
@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain")
    if chain is None:
        return

    try:
        res = await chain.acall({'query': message.content})
        answer = res['result']
        await cl.Message(content=answer).send()
    except Exception as e:
        await cl.Message(content=f"An error occurred: {e}").send()
