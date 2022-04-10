from sqlalchemy.orm import declarative_base

# ----------------------ORM------------------------------------- #
Base = declarative_base()

class TableBase(Base):
    __abstract__ = True

    @classmethod
    def get_columnset(cls): 
        return set([attr for attr in dir(cls) if not attr.startswith("_") and not attr in ("metadata", "registry") and not callable(getattr(cls, attr))])
    
    @classmethod
    def from_dict(cls, kwargs):
        columnset = cls.get_columnset()
        constructor_parms = {}
        for key, value in kwargs.items():
            if key in columnset:
                constructor_parms[key] = value
        return cls(**constructor_parms)

    def to_dict(self):
        columnset = self.get_columnset()
        ret = {}
        for key in columnset:
            ret[key] = getattr(self, key)
        return ret