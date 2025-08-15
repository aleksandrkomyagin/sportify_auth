from sqlalchemy.orm import DeclarativeBase, declared_attr


class BaseModel(DeclarativeBase):
	__abstract__ = True

	@declared_attr.directive
	def __tablename__(self) -> str:
		return f"{self.__name__.lower()}s"
