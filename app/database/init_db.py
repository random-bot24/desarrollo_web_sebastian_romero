from db import Base, engine
from models.models import *

Base.metadata.create_all(bind=engine)
print("Base de datos inicializada correctamente.")



