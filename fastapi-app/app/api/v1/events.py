from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
import psycopg
from psycopg.rows import dict_row

from app.schemas.event import EventOut, EventUpsert
from app.services.db import get_connection

router = APIRouter()


@router.get("/events", response_model=EventOut)
async def get_event(
    conn: Annotated[psycopg.AsyncConnection, Depends(get_connection)],
    event_id: int | None = Query(default=None, alias="id"),
    name: str | None = Query(default=None),
) -> dict[str, Any]:
    if event_id is None and name is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide either id or name.",
        )

    if event_id is not None:
        query = (
            'SELECT id, "name", description, date_insert, date_update '
            "FROM events.event WHERE id = %s"
        )
        params = (event_id,)
    else:
        query = (
            'SELECT id, "name", description, date_insert, date_update '
            'FROM events.event WHERE "name" = %s'
        )
        params = (name,)

    conn.row_factory = dict_row
    async with conn.cursor() as cur:
        await cur.execute(query, params)
        row = await cur.fetchone()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found."
        )

    return row


@router.post("/events", response_model=EventOut, status_code=status.HTTP_200_OK)
async def upsert_event(
    conn: Annotated[psycopg.AsyncConnection, Depends(get_connection)],
    payload: EventUpsert,
) -> dict[str, Any]:
    conn.row_factory = dict_row
    async with conn.cursor() as cur:
        update_query = (
            'UPDATE events.event SET description = %s '
            'WHERE "name" = %s '
            'RETURNING id, "name", description, date_insert, date_update'
        )
        await cur.execute(update_query, (payload.description, payload.name))
        row = await cur.fetchone()

        if row is None:
            insert_query = (
                'INSERT INTO events.event ("name", description) '
                "VALUES (%s, %s) "
                'RETURNING id, "name", description, date_insert, date_update'
            )
            await cur.execute(insert_query, (payload.name, payload.description))
            row = await cur.fetchone()
    await conn.commit()

    return row
