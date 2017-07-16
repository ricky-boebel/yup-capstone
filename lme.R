library(dplyr)
library(lme4)

ses_full = read.csv("/Users/ricky/yup-capstone/data/ses_full.csv")

ses_full_student = read.csv("/Users/ricky/yup-capstone/data/ses_full_student.csv")

logit2prob <- function(logit){
  odds <- exp(logit)
  prob <- odds / (1 + odds)
  return(prob)
}

ses = ses %>%
  group_by(student_id) %>%
  mutate(count = seq(n()))

base.model = glmer(gb_bool ~ 
                    (1|student_id) , data=ses_full , family = binomial,control=glmerControl(optimizer="bobyqa"))



'''ses_full1 = ses_full[ses_full$question_student_count < 45,]#Above 99th percentile
ses_full1[is.na(ses_full1)] <- 0
#ses_full['question_count'] = scale(ses_full['question_count'])
ses_full1['question_student_count_scale'] = scale(ses_full1['question_student_count'])
ses_full1 = ses_full1[ses_full1$gp_sum_scale <3,]#Above 99.6th percentile'''

ses_full1 = ses_full
ses_full1['tut_count_msg_scale'] = scale(ses_full1['tut_count_msg'])
ses_full1 = ses_full1[ses_full1$tut_count_msg_scale <3,]
ses_full1['gp_6'] = ses_full1['gp_6']  + ses_full1['gp_7'] 


ses_full2 = ses_full_student#[ses_full_student$question_student_count < 45,]#Above 99th percentile
ses_full2[is.na(ses_full2)] <- 0
#ses_full['question_count'] = scale(ses_full['question_count'])
ses_full2['question_student_count_scale'] = scale(ses_full2['question_student_count'])
ses_full2['gp_sum_scale'] = scale(ses_full2['gp_sum'])
ses_full2 = ses_full2[ses_full2$gp_sum_scale <3,]#Above 99.6th percentile
ses_full2['tut_count_msg_scale'] = scale(ses_full2['tut_count_msg'])
ses_full2 = ses_full2[ses_full2$tut_count_msg_scale <3,]
ses_full2['stu_count_msg_scale'] = scale(ses_full2['stu_count_msg'])
ses_full2 = ses_full2[ses_full2$stu_count_msg_scale <3,]#Above 99.6th percentile
ses_full2['name_count_scale'] = scale(ses_full2['name_count'])
ses_full2 = ses_full2[ses_full2$name_count_scale <3,]#Above 99.6th percentile
ses_full2$name_count0 = 0
ses_full2$name_count0[ses_full2$name_count == 0] = 1
ses_full2$name_count1 = 0
ses_full2$name_count1[ses_full2$name_count >= 1] = 1
ses_full2$name_count2 = 0
ses_full2$name_count2[ses_full2$name_count >= 2] = 1
ses_full2$name_count3 = 0
ses_full2$name_count3[ses_full2$name_count == 3] = 1
ses_full2$name_count3plus = 0
ses_full2$name_count3plus[ses_full2$name_count >= 3] = 1


base.model2 = glmer(gb_bool ~  (1|tutor_id) ,
                    data=ses_full2 , family = binomial,control=glmerControl(optimizer="bobyqa"))

base.model3 = glmer(gb_bool ~ question_student_count_scale + 
                      (1|tutor_id) , data=ses_full2 , family = binomial, 
                    control=glmerControl(optimizer="bobyqa"))

base.model4 = glmer(gb_bool ~ question_student_count_scale + stu_count_msg_scale + 
                      (1|tutor_id) , data=ses_full2, family = binomial, 
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
base.model5.4 = glmer(gb_bool ~ gp_0 + gp_11 + gp_5 + gp_9 + gp_6 + gp_2
                      + tut_count_msg_scale +
                        (1|student_id) , data=ses_full2 , family = binomial, 
                      control=glmerControl(optimizer="bobyqa"))

base.model5.6 = glmer(gb_bool ~ gp_0 + gp_11 + gp_5 + gp_9 + gp_6 + gp_2
                      + tut_count_msg_scale + name_count0 +
                        (1|student_id) , data=ses_full2 , family = binomial, 
                      control=glmerControl(optimizer="bobyqa"))


base.model5.5a= glmer(gb_bool ~ gp_0 + gp_1 +gp_2
                       + tut_count_msg_scale +
                       (1|student_id) , data=ses_full2 , family = binomial, 
                     control=glmerControl(optimizer="bobyqa"))

base.model5.5= glmer(gb_bool ~ gp_0 + gp_1 +gp_2 +gp_3 +gp_4 +gp_5 +gp_6 +gp_7 +gp_8 +gp_9 +gp_10 +gp_11+gp_12 +
                       + tut_count_msg_scale +
                       (1|student_id) , data=ses_full2 , family = binomial, 
                     control=glmerControl(optimizer="bobyqa"))

base.model5.5a= glmer(gb_bool ~ gp_0 + gp_11 + gp_5
                                      + tut_count_msg_scale +
                                        (1|student_id) , data=ses_full2 , family = binomial, 
                                      control=glmerControl(optimizer="bobyqa"))

#MVP, no name data
base.model5.5b= glmer(gb_bool ~ gp_0 + gp_11 + gp_5 + gp_9 + gp_6 
                      + tut_count_msg_scale +
                        (1|student_id) , data=ses_full1 , family = binomial, 
                      control=glmerControl(optimizer="bobyqa"))

#MVP, no name data
base.model5.6 = glmer(gb_bool ~ gp_0 + gp_11 + gp_5 + gp_9 + gp_6 
                       + tut_count_msg_scale + crf_sum + crp_sum + crb_sum +  
                         (1|student_id) , data=ses_full1, family = binomial, 
                       control=glmerControl(optimizer="bobyqa"))
#MVP with name data
base.model5.8 = glmer(gb_bool ~ gp_0 + gp_11 + gp_5 + gp_9 + gp_6 
                      + tut_count_msg_scale + name_count3plus +
                        (1|student_id) , data=ses_full2 , family = binomial, 
                      control=glmerControl(optimizer="bobyqa"))

#g0 = hard work,
#g11 = almost there
#gp_5 = good job
#gp_9 = keep going
#gp_6 = you got this
#histogram of random effects
hist(ranef(base.model5.4)$student_id[,1])
# 95% confidence intervals
confint(base.model5.4)

#summary with coefficents
summary(base.model5.5b)

#compare each model's reletive fit with anova
anova( base.model5.5c, base.model5.5b)

mean(ses_full2$gp_sum)
sd(ses_full2$gp_sum)

#Log odds e(formula with a one unit increase in fixed effect) / e(formula holding all constant and fixed effects to their zero equivilent)
# https://stats.idre.ucla.edu/other/mult-pkg/faq/general/faq-how-do-i-interpret-odds-ratios-in-logistic-regression/

# Interpret the interaction term  



"hard work
working hard
You're so close
You are so close
Nice effort
Good job
You've got this
You got this
Keep at it
Keep going
Keep trying
Almost there
Yet"