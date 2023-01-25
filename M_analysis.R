library(tidyverse)
library(ggthemes)


uni_people_data <- read_csv('people_output.csv') |>
  group_by(Occupational_group) |>
  summarise(n = n())

total <- sum(uni_people_data[, 'n'])

occupation_bar_plot <- ggplot(data = uni_people_data) +
  aes(x= reorder(Occupational_group, n/total), y = n/total) +
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






