library(dplyr)
library(ggplot2)

dataset <- gapminder::gapminder
dataset <- filter(dataset, country == "Brazil")

formula <- lifeExp ~ pop

# Aplicando MQO
y <- dataset[[formula[[2]]]]
X <- model.matrix(formula, dataset)

X_lin <- t(X)
bt <- solve(X_lin %*% X, tol = 1e-20) %*% X_lin %*% y
bt

# Prevendo
predicted <- X %*% bt

# Calculando resíduos
residuals <- y - predicted
residuals

SSE <- sum(residuals ** 2)
SSE

# Minimizou o erro medio
sum(residuals) #próximo de zero

# Calculando variância do modelo
n <- nrow(dataset)
n

k <- length(formula[[2]])
k

variance <-  ((t(residuals) %*% residuals) / (n - k))[1]
variance

var_cov <- variance * solve(X_lin %*% X, tol = 1e-20)
var_cov

# Erros padrão das estimativas
ep <- diag(sqrt(var_cov))
ep

# Valores das estimativas t
t_value <- bt / ep
t_value

# Probabilidade do valor t tabelado ser maior do que o calculado
p_value <- pt(t_value, df = (n-k), lower.tail = FALSE)
p_value


summary(lm(formula, dataset))

data_new <- data.frame(
  actual = y,
  OLS = predicted,
  pop = dataset["pop"], 
  residuals = residuals
)

ggplot(data_new, aes(pop, actual)) +
  geom_segment(aes(yend = OLS, xend = pop), color = "gold1", size = 1.2) +
  geom_point(color = "steelblue", size = 2) +
  geom_line(color = "gray23", aes(y = OLS)) +
  scale_x_continuous(labels = scales::comma, breaks = scales::extended_breaks(10)) 
