# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias (reemplaza por requirements.txt si es necesario)
COPY requirements.txt .

#Copiar la uri de mongodb
COPY .env ./

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido de la carpeta src en el directorio de trabajo del contenedor
COPY ./src /app/src

# Expone el puerto que usará Flask
EXPOSE 5000

# Define el comando por defecto para ejecutar la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]
