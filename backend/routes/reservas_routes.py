from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from database import get_db
from auth import decode_token

router = APIRouter(prefix="/api/reservas", tags=["Reservas"])


class ReservaRequest(BaseModel):
    horario_id: int
    fecha: str
    asientos: List[int]
    nombre_pasajero: str
    apellidos_pasajero: str
    email_pasajero: str
    dni_pasajero: str


@router.get("/mis-reservas")
def mis_reservas(user_id: int = Depends(decode_token), conn=Depends(get_db)):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT r.id, h.linea, h.origen, h.destino, r.fecha, r.asientos, r.estado, r.localizador
        FROM reservas r
        JOIN horarios h ON h.id = r.horario_id
        WHERE r.usuario_id = %s
        ORDER BY r.fecha DESC
        """,
        (user_id,),
    )
    rows = cur.fetchall()
    cur.close()
    return [
        {
            "id": r[0], "linea": r[1], "origen": r[2], "destino": r[3],
            "fecha": str(r[4]), "asientos": r[5], "estado": r[6], "localizador": r[7],
        }
        for r in rows
    ]


@router.post("/", status_code=201)
def crear_reserva(data: ReservaRequest, user_id: int = Depends(decode_token), conn=Depends(get_db)):
    cur = conn.cursor()

    # Comprobar que los asientos no estén ocupados
    cur.execute(
        "SELECT asientos FROM reservas WHERE horario_id = %s AND fecha = %s AND estado = 'confirmada'",
        (data.horario_id, data.fecha),
    )
    ocupados = []
    for row in cur.fetchall():
        ocupados.extend(row[0])

    conflicto = [a for a in data.asientos if a in ocupados]
    if conflicto:
        raise HTTPException(status_code=409, detail=f"Asientos ya ocupados: {conflicto}")

    import random, string
    localizador = "BV-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

    cur.execute(
        """
        INSERT INTO reservas (usuario_id, horario_id, fecha, asientos, nombre_pasajero,
            apellidos_pasajero, email_pasajero, dni_pasajero, estado, localizador)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'confirmada', %s)
        RETURNING id
        """,
        (
            user_id, data.horario_id, data.fecha, data.asientos,
            data.nombre_pasajero, data.apellidos_pasajero,
            data.email_pasajero, data.dni_pasajero, localizador,
        ),
    )
    reserva_id = cur.fetchone()[0]
    conn.commit()
    cur.close()

    return {"id": reserva_id, "localizador": localizador, "estado": "confirmada"}


@router.delete("/{reserva_id}")
def cancelar_reserva(reserva_id: int, user_id: int = Depends(decode_token), conn=Depends(get_db)):
    cur = conn.cursor()
    cur.execute(
        "UPDATE reservas SET estado = 'cancelada' WHERE id = %s AND usuario_id = %s RETURNING id",
        (reserva_id, user_id),
    )
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    conn.commit()
    cur.close()
    return {"mensaje": "Reserva cancelada correctamente"}