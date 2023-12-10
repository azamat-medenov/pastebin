
def setup_imports() -> None:
    from src.infrastructure.database import models  # noqa init orm models
    from src.application.user.schemas.user import UserDTO
    from src.application.entry.schemas.entry import EntryWithAuthorDTO
    EntryWithAuthorDTO.model_rebuild()
    UserDTO.model_rebuild()
