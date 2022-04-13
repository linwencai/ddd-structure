from sqlalchemy import Column, Integer, MetaData, String, TIMESTAMP, Boolean, text, func, Enum, Text, Table
from sqlalchemy.orm import registry

mapper_registry = registry()
metadata_obj = MetaData()
