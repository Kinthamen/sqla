from sqlalchemy.orm import declared_attr
import sqla.common.session as BaseSession


class SessionMixin:
    _repr_hide = ['created_at', 'updated_at']

    cls_session: BaseSession.SESSION

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def query(cls):
        return cls.cls_session.query(cls)

    @classmethod
    def filter_by_all(cls, **kwargs):
        return cls.query().filter_by(**kwargs).all()

    @classmethod
    def filter_by_first(cls, **kwargs):
        return cls.query().filter_by(**kwargs).first()

    @classmethod
    def all(cls):
        return cls.query().all()

    # @classmethod
    # def serialize_all(cls, items):
    #     if not isinstance(items, list):
    #         return items.serialize()
    #     return [p.serialize() for p in items]

    def save(self):
        session = self.__class__.cls_session
        session.add(self)
        session.commit()
        return self

    def delete(self):
        session = self.__class__.cls_session
        session.delete(self)
        session.commit()
