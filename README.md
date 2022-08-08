# SQLA

This project contains a declarative base with some common mixins. Pre-Structured to avoid circular dependencies.

## Descripton of some files:

1. sqla.internals.declarative_base.py - contains the global instance of sqlalchemy's declarative base
2. sqla.mixins.session_mixin.py - hides session.add/commit actions and some query actions as class methods
3. sqla.mixins.serializer_mixin.py - json auto-serialization mixin with include/exclude/write only features
4. sqla.mixins.audit_mixin.py - adds created/updated audit methods
5. sqla.common.session.py - contains the global instance of the sqlachemy session class used by files in this package
6. sqla.common.bases.py - contains two combinations of mixins (Base, BaseAudit) for use in your models

## Usage

### Making a Model

```python
from sqlalchemy import Column, ForeignKey, Integer, VARCHAR
from sqlalchemy.orm import relationship
from sqla import Base


class Parent(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(10))
    children = relationship("Child")


class Child(Base):
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("parent.id"))

```

### Using a Model

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqla import BaseSession
from my.models.location import MyModel

engine = create_engine('sqlite:///mydatabase.sqlite')
# !important: Set session before any model usage
# it sets the provided session object in the BaseSession
# and does not invoke it. That is done in the mixin methods.
BaseSession.set_session(sessionmaker(engine))

search_params = { 'name': 'Luke' }

# Adding an entry from json.
# Returns Parent instance that was commited to session.
p = Parent.from_json(search_params).save()

# Using the returned object that just got saved
# and serializing it to json.
# NOTE: If someone can help me on this,
# for some reason before you can print the results
# you have to access a member so it populates the results.
print(c.serialize() if c.id else {})

# Querying: get all results based on search_params
# and serialize to json.
p = Parent.serialize_all(Parent.filter_by_all(**search_params))
print(p)

# Querying: get first result based on search_params
# and serialize to json.
p = Parent.serialize_all(Parent.filter_by_first(**search_params))
# or
p = (Parent.filter_by_first(**search_params)).serialize()
print(p)

# Deleting an entry from json.
# Returns Parent instance that was commited to session.
p = (Parent.filter_by_first(**search_params)).delete()

# Querying: using the traditional query from SQLAlchemy
# Note that "query" is invoked. Returns a SQLAlchemy session
# query object.
p = Parent.query().all()
print(p)


# There may be some more examples, but these are the ones I am using.
```

# Contributing

If you can, send me a PR with fixes.
If you can't, create an issue.
