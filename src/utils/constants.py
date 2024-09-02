columns_white_list = [
    'Data de nascimento', 
    'Raça', 
    'Sexo', 
    'Orientação Sexual',
    'Turno', 
    'Período', 
    'Quantidade de disciplinas no período',
    'Origem escolar', 
    'É cotista por renda inferior a 1,5 salário mínimo?',
    'Moradia estudantil', 
    'Em seu endereço atual, como você mora?',
    'Condições de moradia familiar', 
    'Região da moradia', 
    'Material de construção da moradia',
    'Saneamento', 
    'Mudou de endereço para estudar no IFPE',
    'Quantas pessoas compõem o seu núcleo familiar?',
    'Você possui filhos maiores que 6 anos',
    'Você possui filhos entre 0 e 6 anos',
    'Recebe algum tipo de bolsa estudantil',
    'Você é chefe de família ou responsável pela própria subsistência?',
    'Renda bruta familiar', 
    'Renda per capita',
    'Alimentação no ambiente escolar',
    'Como você acessa os serviços de saúde',
    'Como você acessou à educação básica (Ensino Fundamental)',
    'Como você acessa/acessou à educação básica (Ensino Médio)',
    'Relato de vida'
    ]

columns_to_float64 = [
    'Renda bruta familiar', 
    'Renda per capita',
    'Alimentação no ambiente escolar'
    ]

one_hot_encoding_columns = [  #Provavelmente terei que parar de usar essas colunas
    'Raça', 
    'Sexo', 
    'Orientação Sexual',
    'Turno', 
    'Origem escolar', 
    'Em seu endereço atual, como você mora?', 
    'Condições de moradia familiar', 
    'Região da moradia', 
    'Material de construção da moradia', 
    'Saneamento', 
    'Como você acessa os serviços de saúde', 
    'Como você acessou à educação básica (Ensino Fundamental)', 
    'Como você acessa/acessou à educação básica (Ensino Médio)'
    ]