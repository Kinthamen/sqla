from sqlalchemy.orm import declarative_mixin
from sqlalchemy.orm import QueryableAttribute


@declarative_mixin
class SerializerMixin:
    __exclude__ = ('id',)
    __include__ = ()
    __write_only__ = ('created_at', 'updated_at',)

    @classmethod
    def from_json(cls, json, selfObj=None):
        if selfObj is None:
            self = cls()
        else:
            self = selfObj

        exclude = cls.__exclude__ or ()
        include = cls.__include__ or ()

        for prop, value in json.items():
            # ignore all non user data, e.g. only
            if (not (prop in exclude) | (prop in include)) and isinstance(
                    getattr(cls, prop, None), QueryableAttribute):
                setattr(self, prop, value)

        return self

    def deserialize(self, json):
        return self.__class__.from_json(json, selfObj=self)

    @classmethod
    def serialize_list(cls, object_list=[]):
        output = []
        for li in object_list:
            if getattr(li, 'serialize', None):
                output.append(li.serialize())
            else:
                output.append(li)
        return output

    def serialize(self, **kwargs):

        # init write only props
        if len(getattr(self.__class__, '__write_only__', ())) == 0:
            self.__class__.__write_only__ = ()
        dictionary = {}
        expand = kwargs.get('expand', ())
        prop = 'props'
        if expand:
            # expand all the fields
            for key in expand:
                getattr(self, key)
        iterable = self.__dict__.items()
        is_custom_property_set = False
        # include only properties passed as parameter
        if (prop in kwargs) and (kwargs[prop] is not None):
            is_custom_property_set = True
            iterable = kwargs[prop]
        # loop trough all accessible properties
        for key in iterable:
            accessor = key
            if isinstance(key, tuple):
                accessor = key[0]
            if not (accessor in self.__class__.__write_only__) and not accessor.startswith('_'):
                # force select from db to be able get relationships
                if is_custom_property_set:
                    getattr(self, accessor, None)
                if isinstance(self.__dict__.get(accessor), list):
                    dictionary[accessor] = self.__class__.serialize_list(object_list=self.__dict__.get(accessor))
                # check if those properties are read only
                elif getattr(self.__dict__.get(accessor), 'serialize', None):
                    dictionary[accessor] = self.__dict__.get(accessor).serialize()
                else:
                    dictionary[accessor] = self.__dict__.get(accessor)
        return dictionary