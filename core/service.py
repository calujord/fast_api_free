from sqlalchemy.orm import Session


class ServiceBase:
    def __init__(self, session: Session):
        self.session = session
