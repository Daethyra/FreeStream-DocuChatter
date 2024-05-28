# FreeStream

Build your own personal chatbot interface with Streamlit!

***TLDR***:
- A repository to help you get started building your own chatbots using LangChain
- All conversation content is traced via LangSmith for developer evaluation
- Hostable for free through Streamlit Community Cloud
- API keys required
- Pay-per-use ChatGPT style interface

## Table of Contents

- [Quickstart](#quickstart)
  - [Installation](#installation)
- [Description](#description)
  - [Key Concepts](#key-concepts)
  - [What can I do with FreeStream?](#what-can-i-do-with-freestream)
- [Functional Requirements](#functional-requirements)
- [Non-Functional Requirements](#non-functional-requirements)
- [License](./LICENSE)
- [LLM Providers' Privacy Policies](#llm-providers-privacy-policies)

## Quickstart

This app is hosted via Streamlit Community Cloud, [here](https://freestream.streamlit.app/ "Current Version: 4.0.1")

### Installation

This project uses `poetry` for dependency management to be consistent with Streamlit Community Cloud's deployment process.

Install `poetry` with:
```bash
pip install -U pip && pip install -U poetry
```

Then, install the project's dependencies in a virtual environment using `poetry`. 

Run:

```bash
poetry install
```

You will need to set all required secrets, which require their own respective accounts.
Make a copy of "template.secrets.toml" and rename it to "secrets.toml" in the root of the project. Fill out each field in the file.

**Need API Keys?**
| **API Platform** | **Link** |
| ---- | ---------- |
| Claude | https://console.anthropic.com/ |
| Google | https://aistudio.google.com/app/apikey |
| Langchain | https://smith.langchain.com/ |
| OpenAI | https://platform.openai.com/api-keys |

You can then start the development server with hot reloading by running:

```bash
poetry run streamlit run ./freestream/🏡_Home.py
```

---

## Description
I originally created this project as a chatbot for law and medical professionals, but I quickly realized a more flexible system would benefit everyone.

#### **Key Concepts**

*Related to extending the capabilities of generative AI.*
| **Concept** | **Definition** |
| ---- | ---------- |
| [Large Language Model](https://en.wikipedia.org/wiki/Large_language_model "Wikipedia: Large language model") | A model that can generate text. |
| [RAG](https://arxiv.org/abs/2005.11401 "Arxiv: 2005.11401") | Retrieval Augmented Generation |
| [C-RAG](https://arxiv.org/abs/2401.15884 "Arxiv: 2401.15884") | Corrective-Retrieval Augmented Generation |
| [Self-RAG](https://arxiv.org/abs/2310.11511 "Arxiv: 2310.11511") | Self-reflective Retrieval Augmented Generation |
| [ColBERT](https://arxiv.org/abs/2004.12832 "Arxiv: 2004.12832") | Efficient BERT-Based Document Search |
| [RAPTOR](https://arxiv.org/abs/2401.18059 "Arxiv: 2401.18059") | Recursive Abstractive Processing for Tree-Organized Retrieval |

### What can I do with FreeStream?

FreeStream has two chatbots where you can interact with an LLM of your choosing, for example, GPT-4o or Claude Opus. You can very easily add more LLMs to the chatbot dictionary, like Llama 3 via [Ollama](https://ollama.com/ "Ollama home page"), or Gemini-Pro through LangChain's [`ChatGoogleGenerativeAI`](https://api.python.langchain.com/en/latest/chat_models/langchain_google_genai.chat_models.ChatGoogleGenerativeAI.html "LangChain API Docs"). The original chatbot for this project was "RAGbot," which allows you to ask questions about your upload file(s). Curie, is a more for programming and self-learning purposes.

#### Functional Requirements

The application **MUST**...
1. Provide a user interface for chatting with large language models.
2. Have a retrieval augmented generative chatbot.
3. Provide a range of chatbot pages, differentiated by their prompt engineering.
4. Let the user "drop-in" their choice of LLM at any time during a conversation.
5. ~~Allow users to perform image upscaling (PDF, JPEG, PNG) without limits.~~

#### Non-Functional Requirements

The application **SHOULD**...
1. Aim for 24/7 availability.
2. Prioritize ease of navigation
3. Feature a visually appealing, seamless interface.

---

# [License](./LICENSE)

# LLM Providers' Privacy Policies

- [OpenAI Privacy Policy](https://openai.com/policies/privacy-policy)
- [Google](https://transparency.google/our-policies/privacy-policy-terms-of-service/ "Was unable to find a privacy policy specific to Google AI Studio.")
- [Anthropic](https://support.anthropic.com/en/articles/7996866-how-long-do-you-store-personal-data "Support forum response that may suddenly be obsoleted.")
- [Streamlit](https://streamlit.io/privacy-policy/)

