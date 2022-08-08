# SQLA

This project contains a declarative base with some common mixins. Pre-Structured to avoid circular dependencies.

## Usage

### Making a Model

```python
from sqlalchemy import Column, ForeignKey, Integer, VARCHAR
from sqlalchemy.orm import relationship
from sqla.common.bases import Base
from sqla.internals.declarative_base import DECLARATIVE_BASE


class Parent(DECLARATIVE_BASE, Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(10))
    children = relationship("Child")


class Child(DECLARATIVE_BASE, Base):
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
Session = sessionmaker(engine)
# Initialize models by injecting session
# NOTE: We are only passing the session object,
# not invoking it.
MyModel.set_session(Session)

search_params = { 'name': 'Luke' }

# Adding an entry from json.
# Returns MyModel instance that was commited to session.
p = MyModel.from_json(search_params).save()

# Using the returned object that just got saved
# and serializing it to json.
print(c.serialize())

# Querying: get all results based on search_params
# and serialize to list of json.
p = MyModel.serialize_list(Parent.filter_by_all(**search_params))
print(p)

# Querying: get first result based on search_params
# and serialize to json.
p = (MyModel.filter_by_first(**search_params)).serialize()
print(p)

# Deleting an entry from json.
(Parent.filter_by_first(**search_params)).delete()

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
