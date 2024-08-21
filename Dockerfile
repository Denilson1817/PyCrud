#imagen base de Python
FROM python:3.10-slim

#directorio de trabajo para el contenedor
WORKDIR /app

#copia de los requirements
COPY requirements.txt .

#copia de la uri de mongodb
COPY .env ./

#instalacion de dependencias
RUN pip install --no-cache-dir -r requirements.txt

#copia de src -> contenedor
COPY ./src /app/src

#puerto para Flask
EXPOSE 5000

#comando para la ejecución
CMD ["flask", "run", "--host=0.0.0.0"]
