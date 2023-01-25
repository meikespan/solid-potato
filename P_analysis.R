library(tidyverse)
uni_people<-read_csv("uni_people.csv")

profession_N <- uni_people |>
  group_by(`Occupational group`) |>
  summarise(number_of_people=n()) |>
  mutate(percentage=number_of_people / sum(number_of_people))

bargraph_occupation_uni_percentage=ggplot(data=profession_N)+
  aes(x=`Occupational group`, y=percentage)+
  labs(title="Occupational percentages")+
  labs(y="Percentage", x="Occupational group")+
  theme_economist()+
  theme_light()+
  theme(panel.background = element_rect(fill = "snow", colour = "grey50"))+
  geom_bar(stat = "summary", fun = "mean",fill="aquamarine4")

print(bargraph_occupation_uni_percentage)







