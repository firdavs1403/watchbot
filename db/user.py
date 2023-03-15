from sqlalchemy import INTEGER, VARCHAR, DATE, Float
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    # Telegram UserID
    user_id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(VARCHAR(30), unique=True)

    name: Mapped[str] = mapped_column(VARCHAR(30))

    sec_name: Mapped[str] = mapped_column(VARCHAR(30))

    age: Mapped[int] = mapped_column(INTEGER)

    contact: Mapped[int] = mapped_column(INTEGER, unique=True)

    long: Mapped[float] = mapped_column(Float)

    latit: Mapped[float] = mapped_column(Float)

    reg_date: Mapped[datetime] = mapped_column(DATE, default=datetime.now())

    upd_date: Mapped[datetime] = mapped_column(DATE, onupdate=datetime.now())


async def create_user(user_id: int,
                      username: str,
                      name: str,
                      sec_name: str,
                      age: int,
                      contact: int,
                      long: float,
                      latit: float,
                      session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            user = User(
                user_id=user_id,
                username=username,
                name=name,
                sec_name=sec_name,
                age=age,
                contact=contact,
                long=long,
                latit=latit
            )
            try:
                session.add(user)
            except ProgrammingError as e:
                # TODO: add log
                pass
