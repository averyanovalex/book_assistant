import httpx
import os


http_client = httpx.Client(transport=httpx.HTTPTransport(proxy=os.getenv("PROXY_URL")))


def check_not_russian_ip(verbose=False):
    """Checks if current ip is russian and raises an exception."""
    import requests

    response = requests.get("https://ifconfig.me")
    response.raise_for_status()
    ip = response.text.strip()

    response = requests.get(f"https://ipinfo.io/{ip}/json")
    data = response.json()
    country = data.get("country", "")

    if country == "RU":
        raise Exception("Current ip is russian!")

    if verbose:
        return f"Current ip location: {country}"


def get_openai_llm(model="gpt-4o-mini", run_test_question=False):
    """Returns configured OpenAI LLM instance."""
    from langchain.prompts import PromptTemplate
    from langchain_openai import ChatOpenAI

    # check_not_russian_ip(verbose=False)

    template = "Вопрос: {question} Ответ: Дай короткий ответ"
    prompt = PromptTemplate(template=template, input_variables=["question"])

    openai_llm = ChatOpenAI(
        model=model,
        temperature=0.5,
        http_client=http_client,
    )

    if run_test_question:
        llm_chain = prompt | openai_llm
        question = "Когда человек первый раз полетел в космос?"
        print(llm_chain.invoke(question).content)

    return openai_llm


def get_openai_embedding_model(model="text-embedding-ada-002"):
    """Returns configured OpenAI embeddings model."""
    from langchain_openai.embeddings import OpenAIEmbeddings

    # check_not_russian_ip(verbose=False)

    return OpenAIEmbeddings(
        model=model,
        http_client=http_client,
    )
