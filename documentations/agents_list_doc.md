# Available Agents

This document lists the agents currently available in the framework and their primary functions.

- **network_system_agent:** An agent that retrieves network information, analyzes it, and provides actionable recommendations.
- **system_info_agent:** An agent that retrieves and presents system hardware and software information using available tools.
- **query_generation_agent:** An agent that converts user natural language into effective queries (search, database, etc.)
- **rev
 comprehensive reviewer agent that analyzes system and network reports to provide an integrated analysis and recommendations.
- **summarize_agent:** An agent that summarizes provided text or content into a concise, clear summary.
- **single_page_scraper_agent:** an agent the can scrape a single page from the web and return the results in a structured JSON format
- **web_search_agent:** an agent that can search the internet using serper search tool for information and return the results in a structured JSON format
- **team_manager_agent:** A team manager that can manage a team of agents
- **task_planner_agent:** Breaks down natural language user requests into simple, structured sub-tasks as lowercase strings in a JSON array. Separates time/date info and ensures each step is minimal and actionable for other agents to process.
