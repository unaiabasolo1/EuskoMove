from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import get_db
from auth import decode_token

router = APIRouter(prefix="/api/avisos", tags=["Avisos"])


class AvisoRequest(BaseModel):
    tipo: str          # "aviso" | "urgente" | "info"
    titulo: str
    descripcion: str
    lineas: Optional[str] = None


@router.get("/")
def get_avisos(conn=Depends(get_db)):
    cur = conn.cursor()
    cur.execute("SELECT id, tipo, titulo, descripcion, lineas, created_at FROM avisos ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close()
    return [
        {
            "id": r[0], "tipo": r[1], "titulo": r[2],
            "descripcion": r[3], "lineas": r[4], "created_at": str(r[5]),
        }
        for r in rows
    ]


@router.post("/", status_code=201)
def crear_aviso(data: AvisoRequest, user_id: int = Depends(decode_token), conn=Depends(get_db)):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO avisos (tipo, titulo, descripcion, lineas, autor_id) VALUES (%s, %s, %s, %s, %s) RETURNING id",
        (data.tipo, data.titulo, data.descripcion, data.lineas, user_id),
    )
    aviso_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return {"id": aviso_id, "mensaje": "Aviso publicado"}


@router.delete("/{aviso_id}")
def eliminar_aviso(aviso_id: int, user_id: int = Depends(decode_token), conn=Depends(get_db)):
    cur = conn.cursor()
    cur.execute("DELETE FROM avisos WHERE id = %s RETURNING id", (aviso_id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Aviso no encontrado")
    conn.commit()
    cur.close()
    return {"mensaje": "Aviso eliminado"}