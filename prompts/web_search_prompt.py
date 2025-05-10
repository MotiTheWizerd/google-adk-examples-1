web_search_prompt = """
    use the servper_serach_tool to search the web based on the user query.

    *** available tools ***
    - serper_search_tool

    *** instructions ***
    - use the serper_search_tool to search the web based on the provided user query below.
    - return the results in a structured JSON format.
    - always return the response in a structured JSON format.
    here are examples of the expected response:
    {
        "results": [
            {
                "title": "Title of the result",
                "snippet": "Snippet of the result",
                "url": "URL of the result",
                "domain": "Domain of the result"
            }
        ]
    }
    Do not modify the response format.
    return it to the user as is.
    user query:
    {generated_query}
 """

