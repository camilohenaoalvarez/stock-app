from dataclasses import dataclass
from typing import Self

@dataclass(frozen=True)
class Config:
    db_user: str
    db_pass: str
    db_host: str
    db_port: str
    db_name: str

    @classmethod
    def from_environ(cls, os_environ) -> Self:
        return cls(
            db_user=os_environ["USERNAME"],
            db_pass=os_environ["PASSWORD"],
            db_host=os_environ["HOST"],
            db_port=os_environ["PORT"],
            db_name=os_environ["DB_NAME"],
        )
    
    @property
    def connection_string(self) -> str:
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
        )
