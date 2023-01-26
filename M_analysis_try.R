library(tidyverse)
library(ggthemes)


uni_people_data <- read_csv('people_output.csv') |>
  group_by(Occupational_group) |>
  summarise(n = n())

non_uni_people_data <- read_csv('people_output_non_uni.csv') |>
  group_by(Occupational_group) |>
  summarise(n = n()) |>
  mutate(degree_percentage_of_total = ((uni_people_data[, 'n'])/n)*100 ) |>
  mutate(occupation_percentage_of_total = n/(sum(non_uni_people_data[, 'n'])))

total_uni <- sum(uni_people_data[, 'n'])
total_non_uni <- sum(non_uni_people_data[, 'n'])

degree_total_bar_plot <- ggplot(data = non_uni_people_data) +
  aes(x= Occupational_group, y = degree_percentage_of_total$n) +
  geom_col(fill = "aquamarine4") +
  coord_flip() +
  labs(title = 'Distribution of people with degrees over occupational groups', 
       y = 'Percentage with degree of total people', 
       x = 'Occupational group')  +
  theme_igray()+
  theme(panel.grid.major.x = element_line(colour = "grey50",
                                          size = 0.25,
                                          linetype = 1),
        panel.grid.minor.x = element_line(colour = "grey80",
                                          size = 0.25,
                                          linetype = 1))

occupation_total_bar_plot <- ggplot(data = non_uni_people_data) +
  aes(x= Occupational_group, y = occupation_percentage_of_total) +
  geom_col(fill = "aquamarine4") +
  coord_flip() +
  labs(title = 'occupation ', 
       y = 'Percentage of ppl with this occupation of total people', 
       x = 'Occupational group')  +
  theme_igray()+
  theme(panel.grid.major.x = element_line(colour = "grey50",
                                          size = 0.25,
                                          linetype = 1),
        panel.grid.minor.x = element_line(colour = "grey80",
                                          size = 0.25,
                                          linetype = 1))

occupation_bar_plot <- ggplot(data = uni_people_data) +
  aes(x=Occupational_group, y = n/total_uni) +
  geom_col(fill = "aquamarine4") +
  coord_flip() +
  scale_y_continuous(breaks = seq(0,1, by = .1), minor_breaks = seq(0,1, by = .01), labels = scales::label_percent(), limits=c(NA, .3)) +
  labs(title = 'Distribution of people with degrees over occupational groups', 
       y = 'Percentage of total people with a degree', 
       x = 'Occupational group')  +
  theme_igray()+
  theme(panel.grid.major.x = element_line(colour = "grey50",
                                          size = 0.25,
                                          linetype = 1),
        panel.grid.minor.x = element_line(colour = "grey80",
                                          size = 0.25,
                                          linetype = 1))


ggsave('occupation_bar_plot.pdf', plot = occupation_bar_plot, scale = 1, width=7, height=5)
ggsave('occupation_total_bar_plot.pdf', plot = occupation_total_bar_plot, scale = 1, width=7, height=5)
ggsave('degree_total_bar_plot.pdf', plot = degree_total_bar_plot, scale = 1, width=7, height=5)






