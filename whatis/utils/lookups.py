from typing import List
from flask import current_app
from whatis.proxies import db_session
from whatis.models import Whatis
from sqlalchemy import func, and_


def postgres_lookup(input: str) -> List[Whatis]:
    subquery = (
        db_session.query(Whatis.whatis_id, func.max(Whatis.version).label("version"))
        .filter(func.levenshtein(func.lower(Whatis.terminology), input.lower()) < 2)
        .group_by(Whatis.whatis_id)
        .subquery("s2")
    )
    query = db_session.query(Whatis).join(
        subquery,
        and_(
            Whatis.whatis_id == subquery.c.whatis_id,
            Whatis.version == subquery.c.version,
        ),
    )
    return query.all()


def sqlite_lookup(input: str) -> List[Whatis]:
    ...


def lookup_whatis(input: str) -> List[Whatis]:
    dialect = current_app.config.get("DB_DIALECT")

    if dialect == "postgres":
        current_app.logger.debug(f"Using postgres to lookup {input}")
        return postgres_lookup(input)
    elif dialect == "sqlite":
        current_app.logger.debug(f"Using sqlite to lookup {input}")
        return postgres_lookup(input)
    else:
        raise RuntimeError(
            f"Unrecognised SQL dialect {dialect} - I don't even know how you got here!"
        )
