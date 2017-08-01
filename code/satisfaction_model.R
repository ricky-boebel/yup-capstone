library(dplyr)
library(lme4)
library(car)

#Import data, note must run data_srub.py first
ses_full = read.csv("/Users/ricky/yup-capstone/data/ses_full.csv")

#Data cleaning for model
#subseting only successful sessions
ses_full = ses_full[ses_full$gb_bool == 1,]
#dummifying phrases used
ses_full$gp_5[ses_full$gp_5 > 0] = 1 #Good Job
ses_full$gp_11[ses_full$gp_11 > 0] = 1 #Almost there
ses_full$gp_12[ses_full$gp_12 > 0] = 1 #Yet
#scaling the session time variable
ses_full['ses_time_delta_scale'] = scale(ses_full['ses_time_delta'])



#Logistic Mixed Effects Regression Model => Student Dissatisfaction ~ Duration of Session +  Good Job + Almost there + Yet
phrase.model = glmer(student_complained ~  ses_time_delta_scale + gp_5 + gp_11 + gp_12  + #crp_sum + crb_sum + 
                    (1|student_id) , data=ses_full, family = binomial, 
                  control=glmerControl(optimizer="bobyqa"))

#View of results
summary(phrase.model)
