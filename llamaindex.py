import os
from langchain.chat_models import ChatOpenAI
from llama_index import (
    GPTVectorStoreIndex,
    LLMPredictor,
    ServiceContext,
    StorageContext,
    download_loader,
    load_index_from_storage,
    Prompt,
    Document,
    VectorStoreIndex
)
import qdrant_client
from llama_index.vector_stores.qdrant import QdrantVectorStore
import csv
from chatgpt import ChatGPT


class LlamaIndex(object):
    def __init__(self,api_key:str,gpt_model:str) -> None:
        os.environ['OPENAI_API_KEY'] = api_key
        self.llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.2, model_name=gpt_model, openai_api_key=api_key))
        self.service_context = ServiceContext.from_defaults(llm_predictor=self.llm_predictor, chunk_size=1024)
        self.text_list = []
        self.chatgpt = ChatGPT(api_key)
        self.index = None

    def importCSVFile(self,csv_file_path:str):
        with open(csv_file_path, mode='r') as csv_file:
            # Create a CSV reader
            csv_reader = csv.reader(csv_file)
            # Skip the first row (header)
            next(csv_reader)

            # Iterate through the rows and print them
            for row in csv_reader:
                self.text_list.append({"topicNotes":row[1],"summary":row[2]})
        print("len(self.text_list): "+str(len(self.text_list)) + " Loaded")
        # print(self.text_list)

    def buildIndex(self,index_save_path:str,collection_name:str):
        documents = [Document(
                text= t["topicNotes"],
                metadata={
                    "summary": t["summary"]
                }
              )
                for t in self.text_list]

        # build index
        index = VectorStoreIndex.from_documents(documents)
        if not os.path.exists(index_save_path):
            os.makedirs(index_save_path)
        index.storage_context.persist(persist_dir=index_save_path)

        client = qdrant_client.QdrantClient(
            # you can use :memory: mode for fast and light-weight experiments,
            # it does not require to have Qdrant deployed anywhere
            # but requires qdrant-client >= 1.1.1
            location=":memory:"
        )

        storage_context = StorageContext.from_defaults(persist_dir=index_save_path)

        vector_store = QdrantVectorStore(client=client, collection_name=collection_name)
        self.index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context, service_context=self.service_context
        )
        print("Index Build Done")

    def retrieveTopicNotes(self,question):
        self.chatgpt.init_conversation()
        prompt = question + " Do not try to answer the quesion. Can you tell me the related topics or background knowledge about this question?"
        answer = self.chatgpt.continue_conversation(prompt)

        retriever = self.index.as_retriever()
        nodes = retriever.retrieve(question + answer)
        print("Nodes Retriever Done")
        return nodes
    
if __name__ == '__main__':
    api_key = 'sk-'
    gpt_model = 'gpt-3.5-turbo'
    csv_file_path = "demo.csv"
    index_save_path = "index/"
    collection_name = "APCalculus"
    llamaindex = LlamaIndex(api_key,gpt_model)
    llamaindex.importCSVFile(csv_file_path)
    llamaindex.buildIndex(index_save_path,collection_name)

    question= "Determine if the series is absolutely convergent, conditionally convergent, or divergent. \sum_{n=2}^\infty \frac{(-1)^n}{n-1}$"
    nodes = llamaindex.retrieveTopicNotes(question)
    print("Question: "+question)
    print("Topic Notes: "+nodes[0].text)
    print("Summary: "+nodes[0].metadata["summary"])

