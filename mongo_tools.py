import pymongo

class MongoTools:
    def __init__(self, nome_banco, url):
        self.client = pymongo.MongoClient(url)
        self.banco = self.client[nome_banco]

    def __str__(self):
        return f'{self.banco}, Coleções: {self.colecao}'

    #Cria uma coleção
    def create_collection(self, lista_colecoes):
        for colecao in lista_colecoes:
            self.colecao = self.banco[colecao]
            if colecao in self.return_collections():
                self.msg_already_exist = f"A collecion {colecao} já existe no banco."

    #Busca por uma coleção no banco
    def search_collection(self, nome_colecao):
        self.colecao = self.banco[str(nome_colecao)]
        return self.colecao

    #Retorna as coleções existentes
    def return_collections(self):
        self.colecoes_atuais = self.banco.list_collection_names()
        return self.colecoes_atuais

    #Insere dados nas coleções passadas como parametro
    def insert(self, colecoes, doc):

        collections_sucess = []

        for colecao in colecoes:
            self.colecao_atual = self.search_collection(colecao)
            self.colecao_atual.insert_one(doc)
            collections_sucess.append(colecao)
        self.msg_insert_sucess = f'Doc inserted at collections {collections_sucess}'

    #Busca pela query nas coleções passadas como parametro
    def search(self, colecoes, query):

        docs_find = []

        for colecao in colecoes:
            self.colecao_atual = self.search_collection(colecao)
            
            docs = self.colecao_atual.find(query)
            for doc in docs:
                docs_find.append(doc)

        if len(docs_find) == 0:
            raise ValueError("Documento não encontrado")
        else:
            print(docs_find)
            return docs_find      

    #Deleta a primeira ocorrencia 
    def delete(self, colecoes, query):
        for colecao in colecoes:
            self.colecao_atual = self.search_collection(colecao)
            doc_to_delete = self.colecao_atual.find_one(query)

            print(colecoes)

            if doc_to_delete is not None:
                self.colecao_atual.delete_one(doc_to_delete)
                print(f"Documento deletado com sucesso da coleção {self.colecao_atual.name}")
            else:
                print(f'Documento não encontrado na coleção {self.colecao_atual.name}')
    
    #Deleta todos os documentos passados como parametro
    def delete_all(self, colecoes, query):

        docs_to_delete = []

        for colecao in colecoes:
            self.colecao_atual = self.search_collection(colecao)

            docs = self.colecao_atual.find(query)

            for doc in docs:
                docs_to_delete.append(doc)  

            if len(docs_to_delete) == 0:
                raise ValueError("Documento não encontrado")
            else:
                self.colecao_atual.delete_many(docs_to_delete)

    #Vai atualizar apenas a primeira ocorrência
    def update(self, collections, query, new_values):
        collections_updated = []
        collections_not_updated = []

        for collection in collections:
            self.colecao_atual = self.search_collection(collection)

            if self.colecao_atual.find_one(query):
                self.colecao_atual.update_one(query, new_values)
                collections_updated.append(collection)
            else:
                collections_not_updated.append(collection)

        print(collections_updated)
        print(collections_not_updated)






# Código principal
meu_banco = MongoTools('fibrino', 'mongodb://localhost:27017')

#meu_banco.delete(['teste1', 'teste2'], {"nome": "Felipe"})

#meu_banco.update(['teste1', 'teste2', 'teste3'], {"nome": "Felipe"}, {"$set": {"idade": 20}})


meu_banco.insert(["teste3", "teste4"], {"nome": "Lucas", "idade": 19, "sexo": "Feminino"})
