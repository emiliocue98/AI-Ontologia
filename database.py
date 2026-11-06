from motor.motor_asyncio import AsyncIOMotorClient

# URL de conexión a mongodb
MONGO_URL= "mongodb+srv://emiliocue98_db_user:7gDd5dnG1aFrquii@cluster0.djf6luo.mongodb.net/"

# Conexión al cliente
client = AsyncIOMotorClient(MONGO_URL)

# Selección de base de datos
database = client.mibasededatos

# Selección de una colección
collection = database.get_collection("micoleccion")