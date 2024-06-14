## Desenvolvendo a primeira API com FastAPI, pythone docker
## Para adicionar query parameters aos endpoints /atleta para filtrar por nome e CPF:

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

class Atleta(BaseModel):
    nome: str
    cpf: str
    centro_treinamento: str
    categoria: str

# Exemplo de lista de atletas (simulando um banco de dados)
database = [
    Atleta(nome="Atleta 1", cpf="111.111.111-11", centro_treinamento="Centro 1", categoria="Categoria A"),
    Atleta(nome="Atleta 2", cpf="222.222.222-22", centro_treinamento="Centro 2", categoria="Categoria B")
]

@app.get("/atleta")
def get_atletas(nome: str = Query(None), cpf: str = Query(None)):
    results = database
    
    if nome:
        results = [a for a in results if a.nome == nome]
    
    if cpf:
        results = [a for a in results if a.cpf == cpf]
    
    return results

## Para customizar o response de retorno do endpoint /atleta para incluir apenas nome, centro_treinamento e categoria:

from typing import List

class AtletaResponse(BaseModel):
    nome: str
    centro_treinamento: str
    categoria: str

@app.get("/atleta", response_model=List[AtletaResponse])
def get_atletas(nome: str = Query(None), cpf: str = Query(None)):
    results = database
    
    if nome:
        results = [a for a in results if a.nome == nome]
    
    if cpf:
        results = [a for a in results if a.cpf == cpf]
    
    return [{"nome": a.nome, "centro_treinamento": a.centro_treinamento, "categoria": a.categoria} for a in results]

## Para manipular sqlalchemy.exc.IntegrityError e retornar a mensagem customizada:

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

@app.post("/atleta")
def create_atleta(atleta: Atleta):
    try:
        # Simulação de adição ao banco de dados
        database.append(atleta)
        return {"message": "Atleta criado com sucesso"}
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}")
    
    ## Para adicionar paginação utilizando fastapi-pagination com limit e offset:

    from fastapi_pagination import Page, PaginationParams, paginate

@app.get("/atleta", response_model=Page[AtletaResponse])
def get_atletas_paginados(params: PaginationParams = Depends()):
    return paginate(database, params)

