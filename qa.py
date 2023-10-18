"""
Ask questions about a news article using LLMs
"""

import os
import sys
import argparse
from dotenv import load_dotenv
from langchain.document_loaders import SeleniumURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter

def cmdline_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter
                                )
    
    p.add_argument("article", help="URL to article")

    return(p.parse_args())

YELLOW = "\033[0;33m"
GREEN = "\033[0;32m"
WHITE = "\033[0;39m"

def chat_loop(pdf_qa):
    chat_history = []
    print(f"{YELLOW}---------------------------------------------------------------------------------")
    print('Welcome to the DocBot. You are now ready to start interacting with your documents')
    print('---------------------------------------------------------------------------------')
    while True:
        query = input(f"{GREEN}Prompt: ")
        if query == "exit" or query == "quit" or query == "q" or query == "f":
            print('Exiting')
            sys.exit()
        if query == '':
            continue
        result = pdf_qa(
        {"question": query, "chat_history": chat_history})
        print(f"{WHITE}Answer: " + result["answer"])
        chat_history.append((query, result["answer"]))

if __name__ == '__main__':
    load_dotenv('.env')
    args = cmdline_args()


    articles = []
    # Load an article from a URL
    loader = SeleniumURLLoader(urls=[args.article])
    data = loader.load()
    articles.extend(data)

    # Split the documents into smaller chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    articles = text_splitter.split_documents(articles)

    # Convert the document chunks to embedding and save them to the vector store
    # vectordb = Chroma.from_documents(articles, embedding=OpenAIEmbeddings(), persist_directory="./data")
    vectordb = Chroma.from_documents(articles, embedding=OpenAIEmbeddings())
    #vectordb.persist()

    # create our Q&A chain
    pdf_qa = ConversationalRetrievalChain.from_llm(
        ChatOpenAI(temperature=0.7, model_name='gpt-3.5-turbo'),
        retriever=vectordb.as_retriever(search_kwargs={'k': 6}),
        return_source_documents=True,
        verbose=False
    )
    chat_loop(pdf_qa)