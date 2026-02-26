from sqlalchemy import Engine


class BaseService:
    """Base class for services holding shared dependencies"""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
