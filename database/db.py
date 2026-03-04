import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()
database_url = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(database_url)

def xp_requerido(nivel):
    return 5 * (nivel ** 2) + 40 * nivel + 100

def actualizar_xp(user_id, guild_id, xp_obtenida):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT xp, nivel FROM experiencia WHERE user_id = %s AND guild_id = %s", (user_id, guild_id))
    result = cursor.fetchone()
    
    subio_nivel = False
    
    if result:
        xp_actual, nivel_actual = result
        xp_nueva = xp_actual + xp_obtenida
        nivel_nuevo = nivel_actual
        
        while xp_nueva >= xp_requerido(nivel_nuevo):
            xp_nueva -= xp_requerido(nivel_nuevo)
            nivel_nuevo += 1
            subio_nivel = True
        
        cursor.execute("UPDATE experiencia SET xp = %s, nivel = %s WHERE user_id = %s AND guild_id = %s",
                      (xp_nueva, nivel_nuevo, user_id, guild_id))
    else:
        cursor.execute("INSERT INTO experiencia (user_id, guild_id, xp, nivel) VALUES (%s, %s, %s, %s)",
                      (user_id, guild_id, xp_obtenida, 0))
    
    conn.commit()
    cursor.close()
    conn.close()
    return subio_nivel
        

def guardar_sorteo(guild_id, channel_id, message_id, premio, ganadores, termina_en, activo=True):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sorteos (guild_id, channel_id, message_id, premio, ganadores, termina_en, activo) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
                (guild_id, channel_id, message_id, premio, ganadores, termina_en, activo))
    sorteo_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return sorteo_id


def finalizar_sorteo_db(sorteo_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sorteos WHERE id = %s", (sorteo_id,))
    conn.commit()
    cursor.close()
    conn.close()

def obtener_sorteos_activos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, guild_id, channel_id, message_id, premio, ganadores, termina_en FROM sorteos WHERE activo = TRUE")
    sorteos = cursor.fetchall()
    cursor.close()
    conn.close()
    return sorteos

