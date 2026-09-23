from api.core.errors import NotFoundError


class EntryNotFoundError(NotFoundError):
    code = "entry_not_found"
    title = "Entry Not Found"