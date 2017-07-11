library(dplyr)

ses = read.csv("yup-capstone/data/ses_1_42.csv")

ses = ses %>%
  group_by(student_id) %>%
  mutate(count = seq(n()))

base.model = lmer(gb_bool ~ session_count +
                    (1|student_id) + (1|count), data=ses)

summary(base.model)