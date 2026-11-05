from sqlalchemy import CheckConstraint, Integer, Text, Boolean, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Food(Base):
    __tablename__ = "foods"
    __table_args__ = (CheckConstraint("price >= 0", name="foods_price_check"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Integer)
    category: Mapped[str] = mapped_column(Text)
    is_available: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))

