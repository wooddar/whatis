from typing import List

from flask import current_app
from sqlalchemy import func, and_, or_, false

from whatis.models import Whatis
from whatis.proxies import db_session


def postgres_lookup(input: str) -> List[Whatis]:
    subquery_base = db_session.query(
        Whatis.whatis_id, func.max(Whatis.version).label("version")
    )
    subquery_filtered = subquery_base.filter(
        or_(
            func.levenshtein(func.lower(Whatis.terminology), input.lower()) <= 1,
            Whatis.terminology.ilike(f"%{input}%") if len(input) > 3 else false(),
        )
    )
    subquery_grouped = subquery_filtered.group_by(Whatis.whatis_id).subquery("s2")
    query = db_session.query(Whatis).join(
        subquery_grouped,
        and_(
            Whatis.whatis_id == subquery_grouped.c.whatis_id,
            Whatis.version == subquery_grouped.c.version,
        ),
    )
    return query.all()


def sqlite_lookup(input: str) -> List[Whatis]:
    subquery_base = db_session.query(
        Whatis.whatis_id, func.max(Whatis.version).label("version")
    )
    subquery_filtered = subquery_base.filter(
        Whatis.terminology.ilike(f"%{input}%" if len(input) > 3 else f"{input}")
    )
    subquery_grouped = subquery_filtered.group_by(Whatis.whatis_id).subquery("s2")
    query = db_session.query(Whatis).join(
        subquery_grouped,
        and_(
            Whatis.whatis_id == subquery_grouped.c.whatis_id,
            Whatis.version == subquery_grouped.c.version,
        ),
    )
    return query.all()


def lookup_whatis(input: str) -> List[Whatis]:
    dialect = current_app.config.get("DB_DIALECT")

    if dialect == "postgres":
        current_app.logger.debug(f"Using postgres to lookup {input}")
        return postgres_lookup(input)
    elif dialect == "sqlite":
        current_app.logger.debug(f"Using sqlite to lookup {input}")
        return sqlite_lookup(input)
    else:
        raise RuntimeError(
            f"Unrecognised SQL dialect {dialect} - I don't even know how you got here!"
        )


def get_all_whatises() -> List[Whatis]:
    # Return all Whatises to be sent as a CSV
    subquery_base = db_session.query(
        Whatis.whatis_id, func.max(Whatis.version).label("version")
    )
    subquery_grouped = subquery_base.group_by(Whatis.whatis_id).subquery("s2")
    query = (
        db_session.query(Whatis)
        .join(
            subquery_grouped,
            and_(
                Whatis.whatis_id == subquery_grouped.c.whatis_id,
                Whatis.version == subquery_grouped.c.version,
            ),
        )
        .order_by(Whatis.terminology)
    )
    return query.all()
