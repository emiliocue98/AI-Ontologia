from pydantic import BaseModel, Field, ConfigDict, GetCoreSchemaHandler
from pydantic_core import core_schema
from typing import Any, List, Optional
from datetime import datetime
from bson import ObjectId

# Adaptador de tipo personalizado que permite el manejo de ObjectId de MongoDB como cadenas de texto en Pydantic
class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.str_schema()
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(lambda x: str(x))
        )
# ------- Esquemas CRUD --------
class AlumnoBase(BaseModel):
    estudiante_id: str = Field(..., description="ID del estudiante, por ejemplo: al_123")
    nombre: str = Field(..., description="Nombre del estudiante")
    edad: int = Field(..., description="Edad del estudiante")
    genero: str = Field(..., description="masculino/femenino/otro")
    peso: float = Field(..., description="Peso del estudiante en kilogramos")
    estatus: str = Field(..., description="Estatus del estudiante, por ejemplo: activo/inactivo")
    clase_ontologica: str = Field(default="Alumno", description="Clase de ontología a la que pertenece el estudiante")

class AlumnoCreate(AlumnoBase):
    pass # Por definir, se puede agregar validaciones adicionales para la creación de un alumno

class AlumnoResponse(AlumnoBase):
    id: PyObjectId = Field(..., alias="_id", description="ID único del estudiante en la base de datos")
    iri: str = Field(..., description="Identificador de recurso internacional (IRI) del estudiante")
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

# Esquema para profesor
class ProfesorBase(BaseModel):
    profesor_id: str = Field(..., description="Identificador único del profesor, ej. prof_001")
    nombre: str = Field(..., description="Nombre completo")
    categoria: str = Field(default="Titular")
    clase_ontologica: str = Field(default="Profesor")
class ProfesorCreate(ProfesorBase):
    pass
class ProfesorResponse(ProfesorBase):
    id: PyObjectId = Field(alias="_id")
    iri: str = Field(..., description="IRI semántico unívoco")
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

# Esquemas para materia
class MateriaBase(BaseModel):
    materia_id: str = Field(..., description="Clave de la materia, ej. mat_001")
    nombre_materia: str = Field(..., description="Nombre de la asignatura")
    creditos: int = Field(..., ge=1, le=20)
    clase_ontologica: str = Field(default="Materia")
class MateriaCreate(MateriaBase):
    pass
class MateriaResponse(MateriaBase):
    id: PyObjectId = Field(alias="_id")
    iri: str = Field(..., description="IRI semántico unívoco")
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
class SolicitudInscripcion(BaseModel):
    estudiante_id: str = Field(..., description="Identificador del alumno")
    materia_id: str = Field(..., description="Identificador de la materia")
    profesor_id: str = Field(..., description="Identificador del profesor titular")
class ResultadoValidacionSemantica(BaseModel):
    es_valido: bool
    mensaje: str
    detalles_razonador: List[str] = []
    tiempo_razonamiento_ms: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
class TrazaAuditoria(BaseModel):
    solicitud: SolicitudInscripcion
    resultado: ResultadoValidacionSemantica
    agente_emisor: str = "Agente_Validador_Semantico"
    timestamp: datetime = Field(default_factory=datetime.utcnow)