library(data.table)
library(ggplot2)
library(dplyr)
library(titanic)

dataset <- na.omit(as.data.table(titanic_train))
dataset[, Fare := DescTools::Winsorize(Fare, probs = c(0, 0.9))]

ggplot(dataset, aes(Fare, Survived)) +
  geom_point(color = "steelblue") +
  theme_classic()

# Eu poderia já "chutar" um valor para tentar adequar essa reta

betha0 <- -1
betha1 <- 0.03
p = exp(betha0 + betha1 * dataset$Fare) / (1 + exp(betha0 + betha1 * dataset$Fare))
dataset[, prob := p]

ggplot(dataset, aes(Fare, Survived)) +
  geom_point(color = "steelblue") +
  geom_line(aes(y = prob), color = "gray33") +
  geom_hline(yintercept = 0.5, color = "red", size = 0.1) +
  theme_classic() +
  labs(title = "Logistical Regression by hand!")

ggplot(dataset, aes(Fare, log(prob))) +
  geom_line(color = "steelblue") +
  theme_classic() +
  labs(title = "Log of probabilities")

# A Função de verossimilhança seria o produtório de PYy, o log disso resulta em:
LL <- function(betha0, betha1) {
  x = dataset$Fare
  y = dataset$Survived
  p = exp(betha0 + betha1 * x) / (1 + exp(betha0 + betha1 * x))
  -sum(y * log(p) + (1 - y) * log(1 - p))
}

mle = stats4::mle(minuslogl = LL, start = list(betha0 = 0, betha1 = 0))
stats4::summary(mle)

# Que bate com o resultado usando GLM
summary(glm(Survived ~ Fare, family = binomial, dataset))

# A otimização da LL é feita acima, mas poderia tentar aproximar na mão

chutes <- list(
  list(betha0 = 1, betha1 = 0.07, "primeira"),
  list(betha0 = 0, betha1 = 0.06, "segunda"),
  list(betha0 = -0.5, betha1 = 0.05, "terceira"),
  list(betha0 = -0.8, betha1 = 0.04, "quarta"),
  list(betha0 = -1.17949, betha1 = 0.02899, "quinta"),
  list(betha0 = -1.5, betha1 = 0.02, "sexta"),
  list(betha0 = -1.7, betha1 = 0.015, "setima"),
  list(betha0 = -2, betha1 = 0.01, "oitava")
)

data_new <- data.table()

for (chute in chutes) {
  betha0 = chute[[1]]
  betha1 = chute[[2]]
  tentativa = chute[[3]]
  logVer = LL(betha0, betha1)
  p = exp(betha0 + betha1 * dataset$Fare) / (1 + exp(betha0 + betha1 * dataset$Fare))
  temp = data.table(Survived = dataset$Survived, Fare = dataset$Fare, tentativa = tentativa, logVer = round(logVer, 4), prob = p)
  data_new <- rbind(data_new, temp)
}
data_new[, logVer := as.factor(logVer)]

ggplot(data_new, aes(Fare, Survived, group = tentativa)) +
  geom_point(color = "steelblue") +
  geom_line(aes(y = prob, color = logVer)) +
  geom_hline(yintercept = 0.5, color = "red", size = 0.1) +
  theme_classic() +
  labs(title = "Logistical Regression by hand!")

# Calculando os erros padrão do estimador de MLE é feita pela hessiana.
erros_padrao <- sqrt(diag(solve(attr(mle, "details")$hessian)))
erros_padrao

betas <- attr(mle, "coef")
betas

z_values <- betas / erros_padrao
z_values

pnorm(abs(z_values), lower.tail = FALSE)

