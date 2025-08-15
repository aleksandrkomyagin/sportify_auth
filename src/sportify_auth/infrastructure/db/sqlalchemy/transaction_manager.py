from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from sportify_auth.application.protocols.repositories import ITransactionManager


class SqlalchemyTransactionManager(ITransactionManager):
	def __init__(self, session: AsyncSession) -> None:
		self.session = session
		self._transaction: AsyncSessionTransaction | None = None

	async def __aenter__(self) -> "SqlalchemyTransactionManager":
		self._transaction = self.session.begin()
		await self._transaction.__aenter__()
		return self

	async def __aexit__(
		self,
		exc_type: type[BaseException],
		exc_val: BaseException,
		exc_tb: TracebackType,
	) -> None:
		if self._transaction:
			await self._transaction.__aexit__(exc_type, exc_val, exc_tb)

	async def commit(self) -> None:
		if self._transaction:
			await self._transaction.commit()

	async def rollback(self) -> None:
		if self._transaction:
			await self._transaction.rollback()
