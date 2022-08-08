from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
# from flask_security import current_user


class AuditMixin(object):
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    @declared_attr
    def created_by_id(cls):
        return Column(Integer,
            ForeignKey(
                'user.id',
                name=f'fk_{cls.__name__}_created_by_id',
                use_alter=True
            ),
            # nullable=False,
            # default=_current_user_id_or_none
        )

    @declared_attr
    def created_by(cls):
        return relationship(
            'User',
            primaryjoin=f'User.id == {cls.__name__}.created_by_id',
            remote_side='User.id'
        )

    @declared_attr
    def updated_by_id(cls):
        return Column(Integer,
            ForeignKey(
                'user.id',
                name=f'fk_{cls.__name__}_updated_by_id',
                use_alter=True
            ),
            # nullable=False,
            # default=_current_user_id_or_none,
            # onupdate=_current_user_id_or_none
        )

    @declared_attr
    def updated_by(cls):
        return relationship(
            'User',
            primaryjoin=f'User.id == {cls.__name__}.updated_by_id',
            remote_side='User.id'
        )


# def _current_user_id_or_none():
#     try:
#         return current_user.id
#     except:
#         return None