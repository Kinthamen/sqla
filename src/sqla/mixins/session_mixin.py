from sqlalchemy.orm import Session

class SessionMixin:

    @classmethod
    def set_session(cls, session: Session):
        cls.cls_session = session

    @classmethod
    def query(cls):
        return cls.cls_session().query(cls)

    @classmethod
    def filter_by_all(cls, **kwargs):
        return cls.query().filter_by(**kwargs).all()

    @classmethod
    def filter_by_first(cls, **kwargs):
        return cls.query().filter_by(**kwargs).first()

    @classmethod
    def all(cls):
        return cls.query().all()

    def save(self):
        session = self.__class__.cls_session()
        session.add(self)
        session.commit()
        # TODO: Figure out why I need to access a 
        # memeber in order to return the commited object
        return self if self.id else {}

    def delete(self):
        session = self.__class__.cls_session()
        session.delete(self)
        session.commit()
