from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class Departamento(BaseModel):
    nome: str
    sigla: str

class Usuario(BaseModel):
    primeiro_nome: str
    sobrenome: str
    email: str
    tipo_perfil: str
    id_departamento: int

class Recurso(BaseModel):
    nome: str
    status_atual: str

class Disciplina(BaseModel):
    codigo_oficial: str
    nome: str
    id_departamento: int

class ReservaCreate(BaseModel):
    data_reserva: date
    hora_inicio: time
    hora_fim: time
    qtd_participantes_previstos: Optional[int] = None
    finalidade: str
    id_solicitante: int
    id_disciplina: Optional[int] = None
    id_semestre: Optional[int] = None
    # Lista de IDs de recursos a serem reservados
    recursos: list[int]

class ReservaAprovar(BaseModel):
    status_aprovacao: str # 'Aprovada' ou 'Rejeitada'
    justificativa_analise: Optional[str] = None
    id_aprovador: int
