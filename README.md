# Opt_Modeling
Group Project


We will be experimenting with Mean Variance optimization on a rolling basis with a twist.

We will cluster S&P 500 stocks based on correlation over a longer rolling period, but use a Bayesian update sometimes referred to as 'shrinkage' to augment the return vector for each. This will be done by using a stocks clustered mean return over a more recent period as the likelihood for each stocks posterior return and use the 5 year return as the prior. By doing this we hope to capture clusters wth recent momentum either postive or negative as well as mean reversion within clusters.
