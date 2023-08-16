library(ggplot2)
library(data.table)

media <- 0
desvpad <- 1
dados <- data.frame(x = rnorm(1500, media, desvpad))
dados$x <- (dados$x - media) / desvpad

dados$fpd <- (exp(1) ^ (-dados$x)) / (desvpad * (1 + (exp(1) ^ (-dados$x))) ^ 2)

ggplot(dados, aes(x, fpd)) +
  geom_line()

dados$fda <- 1 / (1 + exp(1) ^ -dados$x)

ggplot(dados, aes(x, fda)) +
  geom_line()
