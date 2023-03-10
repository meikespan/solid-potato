library(tidyverse)
library(ggthemes)
library(wesanderson)


#reading in our data and transforming it into useful stuff - bar plot
uni_people_data <- read_csv('people_output.csv') |>
  mutate(Birthyear = as.numeric(Birthyear)) |>
  filter(Birthyear <= 1999 & Birthyear >= 1500, na.rm = TRUE) |>
  group_by(Occupational_group) |>
  summarise(n = n()) |>
  mutate(highlight = c('1', '0', '0', '1', '0', '0', '0', '0', '0', '1', '0', '1', '1', '0'))

  total_uni <- sum(uni_people_data[, 'n'])


#reading in our data and transforming it into useful stuff - area graph 
people_data <- read_csv("people_output_for_area_graph.csv") |>
  mutate(Birthyear = as.numeric(Birthyear)) |>
  filter(Birthyear <= 1999 & Birthyear >= 1500) |>  #filtering for our range of decades
  mutate(Decade = (Birthyear - (Birthyear %% 10)), na.rm=TRUE) |> #flooring each birth-year, leaving us with the decade
  group_by(Occupational_group, Decade) |>
  summarise(number_of_people = n()) |> #counting the number of people per occupational group per decade |>
  group_by(Decade) |>
  mutate(proportion_people = number_of_people / sum(number_of_people)) # adding a column with the percentages
          #calculated by dividing the number of people per group per decade by the total people per decade


#reordering the order of the occupational groups so 'other' appears on top of the stack
reordered_data <- people_data |>
  mutate(Occupational_group = factor(Occupational_group))
    

#plotting respective output into a area graph
area_plot <- ggplot(data = reordered_data) +
  aes(x = Decade, y = proportion_people, fill = Occupational_group, width = 10) +
  labs( y = "Percentage of total college alumni", 
        x = "Birth-year (by decade)", 
        fill = "Occupational group") +
  scale_y_continuous(
        breaks = seq(0,1, by = .1), 
        minor_breaks = seq(0,1, by = .05), 
        labels = scales::label_percent(), 
        limits=c(NA, 1)) +
  scale_x_continuous(breaks = seq(1500,2000, by = 100), 
                     minor_breaks = seq(1500,2000, by = 10)) +
  geom_bar(stat = "identity") +
  scale_fill_manual(
        values = c('#ADB17DFF', '#B1746FFF', '#5B8FA8FF', '#FFB547FF', '#725663FF','#800000FF' )) +
  theme_igray() +
  theme(panel.grid.major.x = element_line(colour = "grey50",
                                            size = 0.25,
                                            linetype = 1),
          panel.grid.minor.x = element_line(colour = "grey80",
                                            size = 0.25,
                                            linetype = 1),
          panel.grid.major.y = element_line(colour = "grey50",
                                            size = 0.25,
                                            linetype = 1),
          panel.grid.minor.y = element_line(colour = "grey80",
                                            size = 0.25,
                                            linetype = 1))

#plotting respective output into a bar plot
occupation_bar_plot <- ggplot(data = uni_people_data) +
  aes(x=reorder(Occupational_group,n/total_uni), y = n/total_uni, fill = highlight) +
  geom_col() +
  coord_flip() +
  scale_y_continuous(
          breaks = seq(0,1, by = .05), 
          minor_breaks = seq(0,1, by = .01), 
          labels = scales::label_percent(), 
          limits=c(NA, .3)) +
  labs( y = 'Percentage of total college alumni', 
        x = 'Occupational group')  +
  scale_fill_manual(values = c("0" = '#B1746FFF',
                               "1" = '#800000FF'))+
  theme_igray()+
  theme(panel.grid.major.x = element_line(colour = "grey50",
                                          size = 0.25,
                                          linetype = 1),
        panel.grid.minor.x = element_line(colour = "grey80",
                                          size = 0.25,
                                          linetype = 1),
        legend.position = "none")

#plotting respective output into a faceted linegraph
faceted_line_graph <- ggplot(data = reordered_data) +
  aes(x= Decade, y = proportion_people, color = Occupational_group) +
  geom_line(linewidth=1.2) +
  facet_wrap(~Occupational_group, nrow = 3 ) +
  scale_color_manual(values = c('#ADB17DFF', '#B1746FFF', '#5B8FA8FF', '#FFB547FF', '#725663FF','#800000FF' )) +
  scale_y_continuous(
        breaks = seq(0,1, by = .2), 
        minor_breaks = seq(0,1, by = .1), 
        labels = scales::label_percent(), 
        limits=c(NA, 1)) +
  scale_x_continuous(
        breaks = seq(1500,2000, by = 100), 
        minor_breaks = seq(1500,2000, by = 20)) +
  labs(y = 'Percentage of total college alumni', 
       x = 'Birth-year (by decade)',
       color = "Occupational group")  +
  theme_igray() +
  theme(panel.grid.major.x = element_line(colour = "grey60",
                                          size = 0.1,
                                          linetype = 1),
        panel.grid.minor.x = element_line(colour = "grey80",
                                          size = 0.1,
                                          linetype = 1),
        panel.grid.major.y = element_line(colour = "grey60",
                                          size = 0.1,
                                          linetype = 1),
        panel.grid.minor.y = element_line(colour = "grey80",
                                          size = 0.1,
                                          linetype = 1),
        legend.position = "none")



ggsave('occupation_bar_plot.pdf', plot = occupation_bar_plot, scale = 1, width=7, height=5)
ggsave('decade_area_graph.pdf', plot = area_plot, scale = 1, width=7, height=5)
ggsave('faceted_line_graph.pdf', plot = faceted_line_graph, scale = 1, width=7, height=5)
