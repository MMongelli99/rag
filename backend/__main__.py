import ollama
from ollama import Client, GenerateResponse
from langchain_community.document_loaders import DirectoryLoader
from langchain_core.documents.base import Document
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.evaluation import load_evaluator
from dotenv import load_dotenv
import os
from datetime import timedelta
from typing import List, Tuple


class DotEnvError(Exception):
    pass


dotenv_loaded: bool = load_dotenv()
if not dotenv_loaded:
    raise DotEnvException

CONTENT_DIR: str = str(os.getenv("CONTENT_DIR"))
CHROMA_DIR: str = str(os.getenv("CHROMA_DIR"))

embedding: OllamaEmbeddings = OllamaEmbeddings(model="nomic-embed-text")

if not os.path.exists(path=CHROMA_DIR):

    # generate embeddings from content

    def load_documents() -> List[Document]:
        loader: DirectoryLoader = DirectoryLoader(path=CONTENT_DIR, glob="*.txt")
        documents: List[Document] = loader.load()
        return documents

    text_splitter: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True,
    )

    documents: List[Document] = load_documents()
    chunks: List[Document] = text_splitter.split_documents(documents=documents)

    db: Chroma = Chroma.from_documents(
        documents=chunks, embedding=embedding, persist_directory=CHROMA_DIR
    )

    print(f"Saved {len(chunks)} chunks to chromadb!")

else:

    db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embedding)


evaluator = load_evaluator(
    evaluator="pairwise_embedding_distance", embeddings=embedding
)
# x = evaluator.evaluate_string_pairs(prediction="apple", prediction_b="orange")
# print(x)

if __name__ == "__main__":
    client: Client = ollama.Client()

    model: str = "llama3.1"

    print(f'Welcome to the {model} chat client! Enter "q" at any time to quit.')

    try:
        while (query := input(f"{model} > ").strip()) != "q":

            results: List[Tuple[Document, float]] = (
                db.similarity_search_with_relevance_scores(query=query, k=3)
            )
            if len(results) == 0:  # or results[0][1] < 0.7:
                print(
                    "Hmm... sorry, I wasn't able to find any relevant results in my knowledge base."
                )
                continue

            context = "".join([doc.page_content for doc, _score in results])

            prompt = f"""
            Can you respond to the following?
            {query}

            ---

            Please answer the query only using the following:
            {context}
            """

            # print("=== PROMPT ===")
            # print(prompt)
            # print("=== END PROMPT ===")

            try:
                res: GenerateResponse = client.generate(model=model, prompt=prompt)
                duration: int = int(
                    int(timedelta(seconds=seconds).total_seconds())
                    if (seconds := (res.eval_duration or 0) // 1_000_000_000)
                    else 0
                )
                took: str = f" (took {duration}s)" if duration > 0 else ""
                print(f"# {model}{took}")
                print(res.response)
            except Exception as e:
                print(e)
    except (EOFError, KeyboardInterrupt):
        pass

    print()
    print(f"Quitting {model} chat client.")
