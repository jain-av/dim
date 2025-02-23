from sqlalchemy import Column, BigInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from dim import db


__all__ = ['SCHEMA_VERSION', 'SchemaInfo']


SCHEMA_VERSION = '12'


class SchemaInfo(db.Model):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    version: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    info: Mapped[str] = mapped_column(Text, nullable=True)  # Text can be None

    @staticmethod
    def current_version():
        # Assuming db.session is available in the 'db' object
        return db.session.execute(db.select(SchemaInfo).limit(1)).scalar_one().version
