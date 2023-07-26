import pymongo

#conectando ao Mongo
cliente = pymongo.MongoClient("mongodb://localhost:27017/")

#criando um banco de dados
meu_banco = cliente['banco_de_dados']


#Verificando se um Banco de Dados existe
print(cliente.list_database_names())

#Criando uma coleção (tabela)
colecao = meu_banco['cientistas']

#Checando se uma coleção existe
print(meu_banco.list_collection_names())

#Inserindo um documento na coleção
cientista = {"nome": "Donald Knuth", "país": "USA"}
c = colecao.insert_one(cientista)
#print(c)

#Inserindo multiplos documentos
lista = [
  { "nome": "Marvin Minsky", "país": "USA"},
  { "nome": "Dennis Ritchie", "país": "USA"},
  { "nome": "Edsger Dijkstra", "país": "Netherlands"},
  { "nome": "Grace Hopper", "país": "USA"},
  { "nome": "John McCarthy", "país": "USA"}
]
l = colecao.insert_many(lista)
#print(l.inserted_ids)

#Buscando dados no MongoDB
busca = colecao.find_one()
#print(busca)

# #Buscando todos os dados
for itens in colecao.find():
    print(itens)


# #Buscando Dados Específicos
# for item in colecao.find({'_id': 1}):
#     print(item)

# #Filtrando por país
# for item in colecao.find({'país': 'USA'}):
#     print(item)

# #Ordenando o Resultado
# doc = colecao.find().sort('nome')
# for d in doc:
#     print(d)

# #Para ordenarmos na ordem inversa, usamos -1 como segundo parâmetro, nossa lista será então ordenada de forma descendente.
# doc = colecao.find().sort('nome', -1)
# # for d in doc:
# #     print(d)


#Deletando Documentos (o método delete_one() somente deleta a primeira ocorrência)
query = {"nome": "Marvin Minsky"}
colecao.delete_one(query)


#Deletando vários Documentos. O método delete_many() para nos auxiliar, que recebe como primeiro parâmetro um objeto query que definirá quais documentos deletar.
minha_query = { "nome" : {"$regex": "^J"} }
d = colecao.delete_many(minha_query)


#Deletando uma Coleção
#colecao.drop()


#Atualizando Coleções
query = { "nome": "Donald Knuth" }
novos_valores = { "$set": { "país": "China"} }
colecao.update_one(query, novos_valores)
for x in colecao.find():
    print(x)


#Atualizando Diversas Coleções
minha_query = { "país": { "$regex": "^U"} }
valores_novos = { "$set": { "país": "Índia" } }
x = colecao.update_many(minha_query, valores_novos)
for itens in colecao.find():
    print(itens)

#O atributo modified_count nos informa quantos documentos foram atualizados:
print(f'Documentos atualizados: {x.modified_count}') # 3


#Limitando o Resultado
limite = colecao.find().limit(3)
for l in limite:
    print(l)
