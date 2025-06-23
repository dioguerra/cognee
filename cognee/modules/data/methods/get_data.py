from uuid import UUID
from typing import Optional
from cognee.infrastructure.databases.relational import get_relational_engine
from ..exceptions import UnauthorizedDataAccessError
from ..models import Data
from ..models.Data import FileProcessingStatus


async def get_data(user_id: UUID, data_id: UUID) -> Optional[Data]:
    """Retrieve data by ID.

    Args:
        user_id (UUID): user ID
        data_id (UUID): ID of the data to retrieve

    Returns:
        Optional[Data]: The requested data object if found, None otherwise
    """
    db_engine = get_relational_engine()

    async with db_engine.get_async_session() as session:
        data = await session.get(Data, data_id)

        if data and data.owner_id != user_id:
            raise UnauthorizedDataAccessError(
                message=f"User {user_id} is not authorized to access data {data_id}"
            )

        return data


async def get_data_status(user_id: UUID, data_id: UUID
                          ) -> Optional[FileProcessingStatus]:
    """get data_id current processing_status.

    Args:
        user_id (UUID): user ID
        data_id (UUID): ID of the data to retrieve

    Returns:
        Optional[FileProcessingStatus]: That status of the requested data
        object if found, None otherwise
    """
    data = await session.get(Data, data_id)

    if data is not None:
        return data.proocessing_status

    return None
