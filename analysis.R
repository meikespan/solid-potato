library(tidyverse)


uni_people_data <- read_csv('uni_people.csv')

summary <- uni_people_data |>
    sapply(function(x) sum(is.na(x)))

print(summary)