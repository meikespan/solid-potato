library(tidyverse)
library(ggthemes)

final_people <- read_csv("people_output.csv") |>
  mutate(Birthyear = as.numeric(Birthyear))

#consolidating the data-set to include a separate column for the number of people in each occupational group
cleaned_final_people <- final_people |>
  filter(Birthyear < 2023 ) |>
  mutate(Century = ceiling(Birthyear/100), na.rm=TRUE) |>
  filter(Century>14) |>
  group_by(Occupational_group, Century) |>
  summarise(number_of_people = n())

profession_proportion <- cleaned_final_people|>
  group_by(Century) |>
  mutate(proportion_people = number_of_people / sum(number_of_people))

line_graph_proportions_per_occupation_per_century<-ggplot(data=profession_proportion)+
  aes(x=Century, y=proportion_people, color=Occupational_group)+
  labs(title="Percentage of college alumni per occupational group per century")+
  labs(y="percentages", x="Century")+
  geom_line()
print(line_graph_proportions_per_occupation_per_century)


ggsave('line_graph_proportions_per_occupation_per_century.pdf', plot=line_graph_proportions_per_occupation_per_century)


