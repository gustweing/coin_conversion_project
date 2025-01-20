# coin_conversion_project

# Arquitetura Escolhida

A arquitetura escolhida para a resolução deste projeto foi a ELT. 
Extrairemos nosso dado de uma API pública, faremos a ingestão destes dados no PostgreSQL e então criaremos algumas tabelas para consumo de negócio. 
Estas tabelas serão consumidas no Power BI para publicação de um Dashboard de negócios. 
Também consumiremos a tabela para a criação de um modelo de clusterização que responda algumas perguntas de negócio. 

![Arquitetura escolhida](images/new_arch.png)