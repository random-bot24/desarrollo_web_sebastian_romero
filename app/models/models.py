from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, DateTime, Text, VARCHAR, Enum
from sqlalchemy.orm import relationship
from database.db import Base, SessionLocal

#Modelos de la base de datos en SQLAlchemy
class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    comunas = relationship("Comuna", back_populates="region")

class Comuna(Base):
    __tablename__ = 'comuna'
    id =Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)
    region = relationship("Region", back_populates="comunas")
    miembros = relationship("Miembro", back_populates="comuna")

class Miembro(Base):
    __tablename__ = 'miembro'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(80), unique=True, nullable=False)
    telefono = Column(VARCHAR(15), nullable=True)
    fecha_registro = Column(DateTime, nullable=False)
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    comuna = relationship("Comuna", back_populates="miembros")
    actividades = relationship("Actividad", back_populates="miembro")

class Actividad(Base):
    __tablename__ = 'actividad'
    id = Column(Integer, primary_key=True, index=True)
    miembro_id = Column(Integer, ForeignKey('miembro.id'), nullable=False)
    dia = Column(Enum('lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'), nullable=False)
    hora_inicio = Column(VARCHAR(5), nullable=False)
    duracion = Column(VARCHAR(5), nullable=False)
    tipo = Column(Enum('arte', 'deporte', 'tecnología', 'social', 'recreación', 'otra'), nullable=False)
    descripcion = Column(Text(500), nullable=True)
    miembro = relationship("Miembro", back_populates="actividades")
    fotos = relationship("Foto", back_populates="actividad")
    nombre = Column(String(255), nullable=False)

class Foto(Base):
    __tablename__ = 'foto'
    id = Column(Integer, primary_key=True, index=True)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)
    ruta_archivo = Column(VARCHAR(300), nullable=False)
    nombre_archivo = Column(VARCHAR(300), nullable=False)
    actividad = relationship("Actividad", back_populates="fotos")


def create_member(nombre, email, telefono, fecha_registro, comuna_id):
    session= SessionLocal()
    nuevo_miembro = Miembro(
        nombre=nombre,
        email=email,
        telefono=telefono,
        fecha_registro=fecha_registro,
        comuna_id=comuna_id
    )
    session.add(nuevo_miembro)
    session.commit()
    session.close()

def get_members():
    session = SessionLocal()
    miembros = session.query(Miembro).all()
    session.close()
    return miembros