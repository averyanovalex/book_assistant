def check_not_russian_ip(verbose=False):
    "Checks if current ip is russian and raises an exception"
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


check_not_russian_ip(verbose=True)


def get_yagpt_llm(run_test_question=False):
    import os

    from langchain_community.llms import YandexGPT
    from langchain.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    yagpt_llm = YandexGPT(
        api_key=os.getenv("YANDEXGPT_API_KEY"),
        folder_id=os.getenv("YANDEXGPT_FOLDER_ID"),
        model_name='yandexgpt',
        temperature=0.5
    )

    if run_test_question:
        template = "What is the capital of {country}?"
        prompt = PromptTemplate.from_template(template)

        chain = prompt | yagpt_llm | StrOutputParser()
        print(chain.invoke({'country': 'Moscow'}))

    return yagpt_llm


def get_openai_llm(model='gpt-4o-mini', run_test_question=False):
    from langchain_openai import ChatOpenAI
    from langchain.prompts import PromptTemplate

    check_not_russian_ip(verbose=False)

    template = "Вопрос: {question} Ответ: Дай короткий ответ"
    prompt = PromptTemplate(template=template, input_variables=["question"])

    openai_llm = ChatOpenAI(model=model, temperature=0.5)

    if run_test_question:
        llm_chain = prompt | openai_llm
        question = "Когда человек первый раз полетел в космос?"
        print(llm_chain.invoke(question).content)

    return openai_llm


def get_openai_embedding_model(model='text-embedding-ada-002'):
    from langchain_community.embeddings import OpenAIEmbeddings

    check_not_russian_ip(verbose=False)

    return OpenAIEmbeddings(model=model)