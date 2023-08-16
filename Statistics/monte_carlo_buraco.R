library(dplyr)

baralho_vermelho <- rep("vermelho", 52)
baralho_azul <- rep("azul", 52)
baralhos <- rbind(baralho_vermelho, baralho_azul)

simulacao <- function(baralhos, ...) {
  embaralha <- sample(baralhos)
  morto_cartas <- embaralha[1:22]
  
  embaralha <- embaralha[22:length(embaralha)]
  
  jogador1 <- c()
  jogador2 <- c()
  jogador3 <- c()
  jogador4 <- c()
  
  jogadores <- c("jogador1", "jogador2", "jogador3", "jogador4")
  
  parar <- FALSE
  while (parar == FALSE) {
    for  (jogador in jogadores) {
      if(length(get(jogador)) == 11) {
        parar = TRUE
        break
      }
      assign(paste(jogador), append(get(jogador), embaralha[1]))
      embaralha = embaralha[-1]
    }
  }
  
  morto1 <- c()
  morto2 <- c()
  
  mortos <- c("morto1", "morto2")
  
  parar <- FALSE
  while (parar == FALSE) {
    for (morto in mortos) {
      if(length(get(morto)) == 11) {
        parar = TRUE
        break
      }
      assign(paste(morto), append(get(morto), morto_cartas[1]))
      morto_cartas = morto_cartas[-1]
    }
  }
  
  testes <- c()
  for (teste in c(jogadores, mortos)) {
    x = mean(get(teste) == "vermelho") == 1 | mean(get(teste) == "azul") == 1
    testes = append(testes, x)
  }
    
  return(any(testes == TRUE))
}

mean(replicate(100000, simulacao(baralhos)))

