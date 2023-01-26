library(tidyverse)
library(ggthemes)
library(hrbrthemes)

final_people <- read_csv("people_output.csv") |>
  mutate(Birthyear = as.numeric(Birthyear))

#consolidating the data-set to include a separate column for the number of people in each occupational group
testing_final_people <- final_people |>
  mutate(Decade = (Birthyear - (Birthyear %% 10)), na.rm=TRUE) |>
  filter(Decade <= 1950 & Birthyear >=1500) |>
  group_by(Occupational_group, Decade) |>
  summarise(number_of_people = n())

testing_profession_proportion <- testing_final_people |>
  group_by(Decade) |>
  mutate(proportion_people = number_of_people / sum(number_of_people))

plot <- ggplot(data=testing_profession_proportion) +
  aes(x = Decade, y = proportion_people, fill = Occupational_group,colour = Occupational_group) +
  labs(title="Percentage of college alumni per occupational group per decade") +
  labs(y = "percentages", x = "Decade")+
  scale_y_continuous(labels = scales::label_percent()) +
  geom_bar(stat="identity")

print(plot)
