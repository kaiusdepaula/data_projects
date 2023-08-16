library(ggplot2)

# Maximum Likelihood Estimation é um método que estima os parametros populacionais
# de forma que a probabilidade (likelihood) dessa estimativa estar certa é máxima.

# Em MLE, assumimos L(theta;x) = f(x | theta)

# O problema matemático se torna mais simples quando assumimos que as observações
# x são independentes e identicamente distribuidas advindas de uma distribuição
# de probabilidade. Reduzindo a função de maxima verossimilhança para:
# L(theta;x) = f(x1,x2,x3,...,xn | theta) = f(x1 | theta)f(x2 | theta)f(x3 | theta)...f(n | theta)
# Aplicando log nos dois lados: LL(theta;x) = f(x1 | theta) + f(x2 | theta) + f(x3 | theta)+ ... +f(n | theta)

# O objetivo então é encontrar o ponto de máximo na função acima, podendo usar
# derivadas primeira e segunda ou técnicas avançadas de otimização.

# Gerando dados de uma distribuição normal
example1 = as.data.frame(list(x = rnorm(25,50,10)))

ggplot(example1, aes(x)) + 
  geom_dotplot(fill = "steelblue") +
  theme_classic()

# A principal parte para o MLE é a definição da função de verossimilhança.
# Nesse caso, o objetivo da MLE será de estimar os parâmetros de média e desv padrão
# da distribuição acima. dnorm(, log = TRUE) já retorna exatamente o logaritmo da verossimilhança

NLL = function(pars, data) {
  # Extract parameters from the vector
  mu = pars[1]
  sigma = pars[2]
  # Calculate Negative Log-LIkelihood
  # Convenciona-se em algoritmos de otimização a minimização de uma função
  # Por isso, basta minimizar o negativo da máxima verossimilhança
  -sum(dnorm(x = data, mean = mu, sd = sigma, log = TRUE))
}

mle = optim(par = c(mu = 40, sigma = 40), fn = NLL, data = example1$x)
mle

# Estimando MLE para coeficientes de uma função de regressão

data <- data.frame(Y = as.matrix(datasets::AirPassengers), date=as.numeric(time(datasets::AirPassengers)))
data["date"] = data["date"] - min(data["date"])


ggplot(data, aes(Y)) +
  geom_density() +
  theme_classic()

ggplot(data, aes(date, Y)) +
  geom_line()

NLL = function(theta0, theta1) {
  # Posso estimar que Y chapeu segue da média da distribuição de poisson
  mu = exp(theta0 + data$date * theta1)
  # Calculate Negative Log-Likelihood
  -sum((data$Y * log(mu)) - mu)
}

mle = stats4::mle(minuslogl = NLL, start = list(theta0 = 90, theta1 = 30))
stats4::summary(mle)

mle_estimates <- attr(mle, "coef")[1] + attr(mle, "coef")[2] * data$date


ols <- lm(Y ~ date, data)
ols
ols_estimates <- as.numeric(ols$fitted.values)

rmse_mle <- sqrt(mean((data$Y - mle_estimates)^2))
rmse_ols <- sqrt(mean((data$Y - ols_estimates)^2))
print(rmse_mle)
print(rmse_ols)

ggplot(data = data, aes(date, Y)) +
  geom_line(aes(y= mle_estimates, color = "MLE")) +
  geom_line(aes(y= ols_estimates, color = "OLS")) +
  geom_point(color = "steelblue")


