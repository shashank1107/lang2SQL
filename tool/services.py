from tool.models import SessionDBConfiguration, NaturalQuery


def fetch_db_tables_from_url_postgres(payload: dict):
    import psycopg2
    conn = psycopg2.connect(payload['db_url'])
    cursor = conn.cursor()
    cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
    query_resp = cursor.fetchall()
    return list(map(lambda x: x[0], query_resp))


def get_db_configuration(session_key):
    config = SessionDBConfiguration.objects.filter(session_key=session_key).first()
    if not config:
        raise ValueError(f"Please refresh the page. Something went wrong!")
    return config


def langchain_sql_chain(config: SessionDBConfiguration, query):
    _DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
    Use the following format:

    Question: "Question here"
    SQLQuery: "SQL Query to run"
    SQLResult: "Result of the SQLQuery"
    Answer: "Final answer here"

    Only use the following tables:

    {table_info}

    If someone asks for the table foobar, they really mean the employee table.

    Question: {input}"""
    # langchain imports
    from langchain import SQLDatabase, SQLDatabaseChain, OpenAI
    from langchain.chains import SQLDatabaseSequentialChain
    from langchain.prompts import PromptTemplate

    PROMPT = PromptTemplate(
        input_variables=["input", "table_info", "dialect"], template=_DEFAULT_TEMPLATE
    )
    llm = OpenAI(temperature=0)
    db_config = config.db_config
    db = SQLDatabase.from_uri(db_config['db_url'], include_tables=db_config['selected_tables'],
                              sample_rows_in_table_info=3)

    # db_chain = SQLDatabaseChain.from_llm(llm, db, prompt=PROMPT, verbose=True, return_intermediate_steps=True)
    db_chain = SQLDatabaseSequentialChain.from_llm(llm, db, verbose=True, return_intermediate_steps=True)
    # response = db_chain.run(query)
    response = db_chain(query)

    # save nl query
    NaturalQuery.objects.create(session_key=config, nl_query=query,
                                sql_query=response["intermediate_steps"][0])

    return response


def langchain_sql_agent(config: SessionDBConfiguration, query):
    from langchain.agents import create_sql_agent
    from langchain.agents.agent_toolkits import SQLDatabaseToolkit
    from langchain import SQLDatabase
    from langchain.llms.openai import OpenAI
    from langchain.agents import AgentExecutor

    db_config = config.db_config
    db = SQLDatabase.from_uri(db_config['db_url'], include_tables=db_config['selected_tables'],
                              sample_rows_in_table_info=3)
    llm = OpenAI(temperature=0)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True
    )
    response = agent_executor.run(query)
    return response
