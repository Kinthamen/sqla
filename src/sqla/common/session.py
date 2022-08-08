from sqlalchemy.orm import Session

SESSION = None

def set_session(session: Session):
    global SESSION
    SESSION = session