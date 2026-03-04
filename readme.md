# NoiceBot

NoiceBot es un bot de Discord multipropósito con sistema de experiencia, moderación, sorteos y comandos utilitarios. Este repositorio está pensado como una **base sólida** para entusiastas que quieran crear y extender su propio bot de Discord, modificando y añadiendo funcionalidades según sus necesidades.

> ⚠️ Este repositorio es una base pública. El desarrollo activo de NoiceBot continúa en un proyecto separado.

---

## Características

- **Sistema de experiencia** — Los usuarios ganan XP por enviar mensajes, con cooldown anti-spam y subida de nivel automática
- **Moderación** — Comandos esenciales para gestionar tu servidor
- **Sorteos** — Sistema de sorteos con persistencia en base de datos, sobrevive reinicios del bot
- **Comandos utilitarios** — Información de servidor, usuarios, avatares y más

---

## Tecnologías

- Python
- discord.py
- PostgreSQL (Supabase)
- psycopg2
- python-dotenv

---

## Configuración

### 1. Clona el repositorio
```bash
git clone https://github.com/beelzegor/noicebot.git
cd noicebot
```

### 2. Instala las dependencias
```bash
pip install -r requirements.txt
```

### 3. Configura las variables de entorno
Crea un archivo `.env` en la raíz del proyecto:
```
DISCORD_TOKEN=tu_token_aqui
DATABASE_URL=tu_cadena_de_conexion_postgresql
```

### 4. Configura la base de datos
Ejecuta las siguientes queries en tu base de datos PostgreSQL:
```sql
CREATE TABLE experiencia (
    user_id TEXT,
    guild_id TEXT,
    xp INTEGER DEFAULT 0,
    nivel INTEGER DEFAULT 0,
    PRIMARY KEY (user_id, guild_id)
);

CREATE TABLE sorteos (
    id SERIAL PRIMARY KEY,
    guild_id TEXT,
    channel_id TEXT,
    message_id TEXT,
    premio TEXT,
    ganadores INTEGER,
    termina_en TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);
```

### 5. Ejecuta el bot
```bash
python main.py
```

---

## Comandos

### Experiencia
| Comando | Descripción |
|---------|-------------|
| `!nivel [@usuario]` | Muestra el nivel y XP del usuario |
| `!leaderboard` | Muestra el ranking de experiencia del servidor |

### Sorteos
| Comando | Descripción |
|---------|-------------|
| `!sorteo <duración> <ganadores> <premio>` | Crea un sorteo (ej: `!sorteo 1h 3 Nitro`) |

### Moderación
| Comando | Descripción |
|---------|-------------|
| `!kick @usuario [razón]` | Expulsa a un usuario |
| `!ban @usuario [razón]` | Banea a un usuario |
| `!tempban @usuario <segundos> [razón]` | Banea temporalmente a un usuario |
| `!mute @usuario` | Silencia a un usuario |
| `!tempmute @usuario <segundos> [razón]` | Silencia a un usuario temporalmente|
| `!clear <cantidad>` | Elimina mensajes del canal |

### Misceláneo
| Comando | Descripción |
|---------|-------------|
| `!ping` | Muestra la latencia del bot |
| `!status` | Muestra el estado del bot |
| `!invite` | Genera el enlace de invitación |
| `!avatar [@usuario]` | Muestra el avatar de un usuario |
| `!serverinfo` | Muestra información del servidor |
| `!userinfo [@usuario]` | Muestra información de un usuario |
| `!say <mensaje>` | Hace que el bot repita un mensaje |

---

## Personalización

El prefijo por defecto es `!` y puede modificarse en `main.py`:

---