# Gestor de partidos y predicciones de la Champions League

Aplicacion web en arquitectura de 3 capas, dockerizada y desplegada en AWS EC2.

## Arquitectura

```
Navegador
   |
   v
[Presentacion]  app/presentation  (rutas Flask + plantillas HTML)
   |
   v
[Logica de negocio]  app/business  (validaciones y reglas)
   |
   v
[Acceso a datos]  app/data  (SQL con psycopg2)
   |
   v
PostgreSQL (volumen Docker pgdata)

Al iniciar:  app/api_client  ->  mockapi (API simulada)  ->  guarda partidos en PostgreSQL
```

Servicios en docker-compose:
- web: la aplicacion Flask (gunicorn), expuesta en el puerto 80.
- db: PostgreSQL 16 con volumen persistente `pgdata`.
- mockapi: API simulada que entrega los partidos (misma imagen, otro comando).

## Flujo de datos

1. Al iniciar, la app crea las tablas y consume `GET /matches` de la API simulada.
2. Los partidos recuperados se almacenan en la tabla `matches`.
3. La pagina principal lista todos los partidos desde la base de datos.
4. El usuario registra una prediccion (resultado y marcador). La capa de negocio valida que el marcador sea coherente con el resultado.
5. La prediccion se guarda en la tabla `predictions`, asociada al partido.
6. La pagina "Predicciones" consulta y muestra todas las predicciones registradas.

## Variables de entorno

Copiar `.env.example` a `.env` y ajustar valores:

| Variable | Descripcion |
|---|---|
| DOCKERHUB_USER | Usuario de Docker Hub para nombrar la imagen |
| DB_HOST, DB_PORT | Host y puerto de PostgreSQL (db, 5432) |
| DB_NAME, DB_USER, DB_PASSWORD | Credenciales de la base de datos |
| MATCHES_API_URL | URL de la API de partidos |
| SECRET_KEY | Clave de sesion de Flask |

## Ejecucion local

```
cp .env.example .env
docker compose up -d --build
```
Abrir http://localhost

## Publicar la imagen en Docker Hub

```
docker login
docker compose build
docker compose push web
```

## Despliegue en AWS EC2

1. Lanzar una instancia EC2 (Ubuntu, t3.small, 20 GiB) con puertos 22 y 80 abiertos en el grupo de seguridad.
2. Conectarse e instalar Docker:
   ```
   sudo apt update
   sudo apt install -y docker.io docker-compose-v2
   sudo systemctl enable --now docker
   sudo usermod -aG docker ubuntu
   ```
3. Clonar el repositorio y crear el `.env`:
   ```
   git clone <URL_DEL_REPOSITORIO>
   cd champions
   cp .env.example .env
   nano .env
   ```
4. Levantar los servicios:
   ```
   docker compose up -d --build
   docker ps
   ```
5. Abrir `http://<IP_PUBLICA_DE_LA_EC2>`.

## Persistencia

Los datos de PostgreSQL se guardan en el volumen `pgdata`. Para comprobarlo:
```
docker compose down
docker compose up -d
```
Los partidos y las predicciones siguen disponibles.
