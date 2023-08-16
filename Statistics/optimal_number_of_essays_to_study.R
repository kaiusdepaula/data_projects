library(data.table)
library(ggplot2)
library(parallel)

nucleos <- detectCores(logical = FALSE)
cl <- makeCluster(nucleos, type = "FORK")

numero_de_vezes <- 10000

jogo <- function(temas = 1:69, preguica = 20) {
  escolha <- sample(temas, preguica)
  selecionados <- sample(temas, 4)
  temp <- any(escolha %in% selecionados)
  return(temp)
}

dados <- data.table()
for (numero_temas in 0:69) {
  total <- clusterApplyLB(cl, x = rep(list(1:69), numero_de_vezes), fun = jogo, preguica = numero_temas)
  temp <- data.table(temas_estudados = numero_temas, probabilidade_de_cair = mean(unlist(total)))
  dados <- rbind(dados, temp)
}

ggplot(dados, aes(temas_estudados, probabilidade_de_cair)) +
  geom_line(color = "steelblue") +
  theme_classic() +
  labs(x = "Temas estudados para a prova", y = "Chance de cair algum dos temas estudados", title = "Simulações de Monte Carlo para o problema de estudos de redação.") +
  scale_x_continuous(n.breaks = 10) +
  scale_y_continuous(labels = scales::label_percent())


