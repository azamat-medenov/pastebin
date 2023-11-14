
def setup_imports() -> None:
    from src.infrastructure.database import models  # noqa init orm models
    from src.application.user.schemas.user import UserSchema
    from src.application.entry.schemas.entry import EntrySchema
    EntrySchema.model_rebuild()
    UserSchema.model_rebuild()
