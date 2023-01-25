library(tidyverse)
library(ggthemes)
uni_people<-read_csv("people_output.csv")

profession_N <- uni_people |>
  group_by(`Occupational_group`) |>
  summarise(number_of_people=n()) |>
  mutate(percentage=number_of_people / sum(number_of_people))

bargraph_occupation_uni_percentage=ggplot(data=profession_N)+
  aes(x=`Occupational_group`, y=percentage)+
  labs(title="Percentage of college alumni per occupational group")+
  labs(y="Percentage of college alumni", x="Occupational group")+
  scale_y_continuous (labels = scales::label_percent())+
  theme_economist()+
  theme_light()+
  theme(panel.background = element_rect(fill = "snow", colour = "grey50"))+
  geom_bar(stat = "summary", fun = "mean",fill="aquamarine4")


ggsave('occupationalgroup_vs_percentage_of_alumni.pdf', plot=bargraph_occupation_uni_percentage, scale=1, width=5, height=7)













