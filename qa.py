#!/usr/bin/env python3
"""
Ask questions about a news article using LLMs
"""

import sys
import argparse
from dotenv import load_dotenv
from langchain.document_loaders import SeleniumURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter

def cmdline_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter
                                )
    
    p.add_argument("article", help="URL to article")
    p.add_argument("-v", "--verbose", action="store_true", default=False,
                   help="enable verbose output")

    return(p.parse_args())

YELLOW = "\033[0;33m"
GREEN = "\033[0;32m"
WHITE = "\033[0;39m"

def chat_loop(qa_chain):
    while True:
        query = input(f"{GREEN}Prompt: ")
        if query == "exit" or query == "quit" or query == "q" or query == "f":
            print(f'{WHITE}Exiting')
            sys.exit()
        if query == '':
            continue
        result = qa_chain(
        {"question": query})
        print(f"{WHITE}Answer: " + result["answer"])

if __name__ == '__main__':
    load_dotenv('.env')
    args = cmdline_args()


    articles = []
    # Load an article from a URL
    loader = SeleniumURLLoader(urls=[args.article])
    data = loader.load()
    articles.extend(data)

    title = data[0].metadata['title']
    source = data[0].metadata['source']

    # Split the documents into smaller chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    articles = text_splitter.split_documents(articles)

    # Convert the document chunks to embedding and save them to the vector store
    # vectordb = Chroma.from_documents(articles, embedding=OpenAIEmbeddings(), persist_directory="./data")
    vectordb = Chroma.from_documents(articles, embedding=OpenAIEmbeddings())
    #vectordb.persist()

    # create our Q&A chain
    prompt_template = """Use the following pieces of context to answer the question at the end in the style of the character Tom Servo from MST3k. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    
    {context}
    
    Question: {question}
    Helpful Answer:"""
    prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)
    llm = ChatOpenAI(temperature=0.7, model_name='gpt-3.5-turbo', verbose=args.verbose)
    article_qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectordb.as_retriever(search_kwargs={'k': 6}),
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": prompt},
        verbose=args.verbose
    )
    article_qa.memory = ConversationBufferMemory(memory_key='chat_history', 
                                                 return_messages=True, 
                                                 output_key='answer')
    print(f"{YELLOW}---------------------------------------------------------------------------------")
    print('Welcome to ArticleBot.  You can ask questions about the following:')
    print(f'Article: {title}')
    print(f'Source: {source}')
    print('---------------------------------------------------------------------------------')
    chat_loop(article_qa)