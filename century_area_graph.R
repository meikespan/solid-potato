library(tidyverse)
library(ggthemes)
library(hrbrthemes)

final_people <- read_csv("people_output.csv") |>
  mutate(Birthyear = as.numeric(Birthyear))

#consolidating the data-set to include a separate column for the number of people in each occupational group
cleaned_final_people <- final_people |>
  filter(Birthyear < 2023 ) |>
  mutate(Century = ceiling(Birthyear/100), na.rm=TRUE) |>
  filter(Century>14 ) |>
  group_by(Occupational_group, Century) |>
  summarise(number_of_people = n())

profession_proportion <- cleaned_final_people|>
  group_by(Century) |>
  mutate(proportion_people = number_of_people / sum(number_of_people))


plot_century <- ggplot(data=testing_profession_proportion) +
  aes(x = Century, y = proportion_people, fill = Occupational_group,colour = Occupational_group) +
  labs(title="Percentage of college alumni per occupational group per century") +
  labs(y = "percentages", x = "Century")+
  scale_y_continuous(labels = scales::label_percent()) +
  geom_bar(stat="identity")

print(plot_century)


ggsave('line_graph_proportions_per_occupation_per_century.pdf', plot=line_graph_proportions_per_occupation_per_century, scale=1, width=5, height=15) 


