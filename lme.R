library(dplyr)
library(lme4)

ses_full = read.csv("/Users/ricky/yup-capstone/data/ses_full.csv")

ses_full_student = read.csv("/Users/ricky/yup-capstone/data/ses_full_student.csv")

ses = ses %>%
  group_by(student_id) %>%
  mutate(count = seq(n()))

base.model = glmer(gb_bool ~ 
                    (1|student_id) , data=ses_full , family = binomial,control=glmerControl(optimizer="bobyqa"))



ses_full1 = ses_full[ses_full$question_student_count < 45,]#Above 99th percentile
ses_full1[is.na(ses_full1)] <- 0
#ses_full['question_count'] = scale(ses_full['question_count'])
ses_full1['question_student_count_scale'] = scale(ses_full1['question_student_count'])

ses_full2 = ses_full_student#[ses_full_student$question_student_count < 45,]#Above 99th percentile
ses_full2[is.na(ses_full2)] <- 0
#ses_full['question_count'] = scale(ses_full['question_count'])
ses_full2['question_student_count_scale'] = scale(ses_full2['question_student_count'])
ses_full2['gp_sum_scale'] = scale(ses_full2['gp_sum'])
ses_full2 = ses_full2[ses_full2$gp_sum_scale <3,]#Above 99.6th percentile
ses_full2['tut_count_msg_scale'] = scale(ses_full2['tut_count_msg'])
ses_full2 = ses_full2[ses_full2$tut_count_msg_scale <3,]#Above 99.6th percentile
ses_full2['name_count_scale'] = scale(ses_full2['name_count'])
ses_full2 = ses_full2[ses_full2$name_count_scale <3,]#Above 99.6th percentile

base.model2 = glmer(gb_bool ~  (1|tutor_id) ,
                    data=ses_full1 , family = binomial,control=glmerControl(optimizer="bobyqa"))

base.model3 = glmer(gb_bool ~ question_student_count_scale +
                      (1|tutor_id) , data=ses_full1 , family = binomial, 
                    control=glmerControl(optimizer="bobyqa"))

base.model4 = glmer(gb_bool ~ question_student_count_scale + gp_rate +
                      (1|student_id) , data=ses_full1 , family = binomial, 
                    control=glmerControl(optimizer="bobyqa"))

base.model5.1 = glmer(gb_bool ~ 
                      (1|student_id) , data=ses_full2 , family = binomial, 
                    control=glmerControl(optimizer="bobyqa"))


base.model5.2 = glmer(gb_bool ~ gp_sum_scale + 
                        (1|student_id) , data=ses_full2 , family = binomial, 
                      control=glmerControl(optimizer="bobyqa"))

#MVP
base.model5.3 = glmer(gb_bool ~ gp_sum_scale + tut_count_msg_scale +
                        (1|student_id) , data=ses_full2 , family = binomial, 
                      control=glmerControl(optimizer="bobyqa"))

#name has some conitation to miscommunication or student inaction
base.model5.4 = glmer(gb_bool ~ gp_sum_scale + tut_count_msg_scale + name_count_scale +
                        (1|student_id) , data=ses_full2 , family = binomial, 
                      control=glmerControl(optimizer="bobyqa"))


summary(base.model5.4)

anova(base.model5.3 , base.model5.4)

mean(ses_full2$gp_sum)
sd(ses_full2$gp_sum)

logit2prob <- function(logit){
  odds <- exp(logit)
  prob <- odds / (1 + odds)
  return(prob)
}

#Log odds e(formula with a one unit increase in fixed effect) / e(formula holding all constant and fixed effects to their zero equivilent)
# https://stats.idre.ucla.edu/other/mult-pkg/faq/general/faq-how-do-i-interpret-odds-ratios-in-logistic-regression/