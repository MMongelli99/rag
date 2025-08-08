# Local Python RAG CLI

This project is a simple setup for RAG (Retrieval Augmented Generation) using a
local LLM.

This project serves as a good starting point for those looking to start building
chat bots using a custom corpus, and can be easily adapted for more complex
uses.

The main application is a simple text input allowing the user to prompt a local
Ollama model.

Plain text files can be added to the content directory to provide context to the
LLM.

The model will then then attempt to find content relevant to the user's prompt
to generate a response.

## Getting Started

This project use's [devenv](https://devenv.sh/) to ensure that all necessary
dependencies and configuration are present while in the project's development
environment.

0. Globally install Ollama, the llama3.1 model, and setup embeddings with
   `ollama run nomic-embed-text`.
1. Install devenv by following its
   [Getting Started](https://devenv.sh/getting-started/) guide.
2. Clone this repo.
3. In the root of the project, run `devenv shell` to activate the development
   environment, which will install all project dependencies and drop you into an
   isolated bash shell. Neovim and some other utilities are present for
   convenience. The environment is hermetic except for the $HOME environment
   variable so that the globally installed Ollama model can be accessed.
4. Upload the text files you wish to provide as context to the content
   directory.
5. Run `python -m backend`. If the ChromaDB directory is not present yet,
   embeddings will be generated for all the context you've uploaded.
6. In another shell, repeat step 3., then run `devenv up` to start the Ollama
   server, which needs to be running so the chat CLI can query it for responses.
7. Back in the first devenv shell, run `python -m backend` to enter the chat
   CLI.
8. Prompt the model about your data! Play around with the model you're using,
   adjust the similarity relevance threshold, try using files other than plain
   text, etc.

> Side Note: The more hermetic (isolated) your development environments are from
> your global system, the more portable your project will be to other's
> machines. This is good practice, but that said, if this is not a concern of
> yours, you can easily scrap all the devenv setup and run this project with
> whatever if your preferred method for setting up python projects.
