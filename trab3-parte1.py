
import random
import matplotlib.pyplot

# variaveis globais
INTERVALO = [-10, 10]
TAM_POPULACAO = 4
TAXA_CROSSOVER = 0.6
TAXA_MUTACAO = 0.01
NUM_GERACOES = 5
MELHOR_APTIDAO = 10000000
MELHOR_INDIVIDUO = []


# funcao que calcula o fitness
def calc_funcao(x):
	return (x**2) - (3*x) + 4
	

# funcao que converte para decimal e decodifica o valor de x
def decodifica(individuo):
	global INTERVALO
	global MELHOR_X
	
	base_10 = 0
	n = 9
	for i in range(10):
		base_10 =  base_10 + (2**n * individuo[i])
		n = n -1
	
	x = INTERVALO[0] + ((INTERVALO[1] - INTERVALO[0]) * (base_10 / (2**10  - 1)))
	
	if x < INTERVALO[0]:
		x = INTERVALO[0]
		
	if x > INTERVALO[1]:
		x = INTERVALO[1]
	
	return x


# funcao que cria a populacao inicial
def cria_populacao_inicial():
	global TAM_POPULACAO
	
	populacao = []
	for i in range(TAM_POPULACAO):
		individuo = []
		for j in range(10):
			individuo.append(random.randint(0,1))
		populacao.append(individuo)
	
	return populacao


# funcao que seleciona os pais
def seleciona_pais(populacao):
	global TAM_POPULACAO
	global MELHOR_APTIDAO
	global MELHOR_INDIVIDUO
	
	# cria uma lista de aptidao da populacao
	fitness_pais = []
	for i in populacao:
		aptidao = calc_funcao(decodifica(i))
		fitness_pais.append(aptidao)
		# atualiza o melhor individuo
		if aptidao < MELHOR_APTIDAO:
			MELHOR_APTIDAO = aptidao
			MELHOR_INDIVIDUO = i
	
	pais = []
	for i in range(TAM_POPULACAO//2):
		individuos = []
		# escolher aleatoriamente dois individuos da populacao
		for j in range(2):
			individuo_1 = random.randint(0, TAM_POPULACAO-1)
			individuo_2 = random.randint(0, TAM_POPULACAO-1)
			
			# atraves do indice dos individuos eh possivel achar o melhor individuo consultando a lista de aptidoes (fitness_pais)
			if fitness_pais[individuo_1] < fitness_pais[individuo_2]:
				individuos.append(list(populacao[individuo_1]))
			else:
				individuos.append(list(populacao[individuo_2]))
				
		pais.append(individuos)
		
	return pais
	

# funcao que aplica crossover e mutacao
# atualiza a populacao atual
def gera_filhos(pais):
	global TAXA_CROSSOVER
	global TAXA_MUTACAO
	
	filhos = []
	
	for i in range(len(pais)):
		pai_1 = pais[i][0]
		pai_2 = pais[i][1]
		prob_crossover = random.random()
		
		# se a probabilidade gerada for menor que a taxa de crossover os filhos se tornam copias dos pais 
		if prob_crossover < TAXA_CROSSOVER:
			gene = random.randint(0, len(pais[0]))
			filho_1 = pai_1[:gene] + pai_2[gene:]
			filho_2 = pai_2[gene:] + pai_1[:gene]
		else:
			filho_1 = pai_1
			filho_2 = pai_2
		
		# aplica mutacao em cada filho
		mutacao(filho_1)
		mutacao(filho_2)

		filhos.append(filho_1)
		filhos.append(filho_2)
	
	return filhos
		

# funcao que aplica mutacao em cada individuo
def mutacao(individuo):
	for i in range(len(individuo)):
		prob_mutacao = random.random()
		if prob_mutacao < TAXA_MUTACAO:
			if individuo == 0:
				individuo == 1
			else:
				individuo == 0
	return individuo
	

def main():
	global NUM_GERACOES
	global MELHOR_APTIDAO
	global MELHOR_INDIVIDUO
	
	populacao = cria_populacao_inicial()
	
	aptidao = []		# lista com a melhor aptidao de cada geracao
	soma = 0 			# variavel para calcular a media do melhor valor de x de cada geracao
	
	for i in range(NUM_GERACOES):
		pais = seleciona_pais(populacao)
		populacao = gera_filhos(pais)
		aptidao.append(MELHOR_APTIDAO)
		soma = soma + decodifica(MELHOR_INDIVIDUO)
	
	matplotlib.pyplot.plot(aptidao)
	matplotlib.pyplot.show()
	
	print("Valor f(x):", MELHOR_APTIDAO)
	print("Média valor de x:", (soma/NUM_GERACOES))
	print("Melhor valor de x:", decodifica(MELHOR_INDIVIDUO))
	
	return 0
	
		
if __name__ == '__main__':
	main()
