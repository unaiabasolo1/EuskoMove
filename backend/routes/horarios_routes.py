from fastapi import APIRouter, Depends
from database import get_db

router = APIRouter(prefix="/api/horarios", tags=["Horarios"])


@router.get("/")
def get_horarios(origen: str = None, destino: str = None, fecha: str = None, conn=Depends(get_db)):
    cur = conn.cursor()
    query = """
        SELECT h.id, h.linea, h.origen, h.destino, h.hora_salida, h.hora_llegada, h.plazas_totales,
               h.plazas_totales - COUNT(r.id) AS plazas_libres
        FROM horarios h
        LEFT JOIN reservas r ON r.horario_id = h.id AND r.fecha = %s AND r.estado = 'confirmada'
        WHERE 1=1
    """
    params = [fecha or "today"]

    if origen:
        query += " AND h.origen ILIKE %s"
        params.append(f"%{origen}%")
    if destino:
        query += " AND h.destino ILIKE %s"
        params.append(f"%{destino}%")

    query += " GROUP BY h.id ORDER BY h.hora_salida"
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()

    return [
        {
            "id": r[0], "linea": r[1], "origen": r[2], "destino": r[3],
            "hora_salida": str(r[4]), "hora_llegada": str(r[5]),
            "plazas_totales": r[6], "plazas_libres": r[7],
        }
        for r in rows
    ]