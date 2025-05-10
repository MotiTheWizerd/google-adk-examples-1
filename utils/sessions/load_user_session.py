from google.adk.sessions import DatabaseSessionService

def load_user_session(app_name: str, user_id: str, session_id: str, intial_state: dict = ""):
    # ********** DATABASE SETUP **********
    db_url = "sqlite:///db_parallel_agent.db"
    session_service = DatabaseSessionService(db_url)
    # ********** END OF DATABASE SETUP **********

    # ********** SESSION SETUP **********
    
    # is_session_exists = session_service.list_sessions(app_name=APP_NAME, user_id=USER_ID)
    # print(is_session_exists)
    session = session_service.get_session(app_name=app_name, user_id=user_id, session_id=session_id)
   
    exists_session_id = session_id
    if session is None:
       session_service.create_session(app_name=app_name, user_id=user_id, session_id=session_id, state=intial_state)
       
    else:
       exists_session_id = session.id
       print("Loaded existing session, state updated:", session.id)
    # ********** END OF SESSION SETUP **********

    return {
       "session_id": exists_session_id,
       "session_service": session_service
    }