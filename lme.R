library(dplyr)
library(lme4)
library(car)

ses_full = read.csv("/Users/ricky/yup-capstone/data/ses_full.csv")

ses_full_student = read.csv("/Users/ricky/yup-capstone/data/ses_full_student.csv")

logit2prob <- function(logit){
  odds <- exp(logit)
  prob <- odds / (1 + odds)
  return(prob)
}

ses_full = ses_full %>%
  group_by(student_id) %>%
  mutate(count = seq(n()))

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
ses_full1 = ses_full1[ses_full1$tut_count_msg_scale <4,]
ses_full1['gp_6'] = ses_full1['gp_6']  + ses_full1['gp_7'] 
ses_full1['ses_num_order_scale'] = scale(ses_full1['ses_num_order'])


ses_full2 = ses_full_student#[ses_full_student$question_student_count < 45,]#Above 99th percentile
ses_full2[is.na(ses_full2)] <- 0
#ses_full['question_count'] = scale(ses_full['question_count'])
ses_full2['question_student_count_scale'] = scale(ses_full2['question_student_count'])
ses_full2['gp_sum_scale'] = scale(ses_full2['gp_sum'])
ses_full2 = ses_full2[ses_full2$gp_sum_scale <4,]#Above 99.6th percentile
ses_full2['tut_count_msg_scale'] = scale(ses_full2['tut_count_msg'])
ses_full2 = ses_full2[ses_full2$tut_count_msg_scale <4,]
ses_full2['stu_count_msg_scale'] = scale(ses_full2['stu_count_msg'])
ses_full2 = ses_full2[ses_full2$stu_count_msg_scale <4,]#Above 99.6th percentile
ses_full2['name_count_scale'] = scale(ses_full2['name_count'])
ses_full2 = ses_full2[ses_full2$name_count_scale <4,]#Above 99.6th percentile
ses_full2['gp_6'] = ses_full2['gp_6']  + ses_full2['gp_7'] 
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

#MVP, gap bridged phrases,no name data
# Key Take away: division between "almost there/keep going" negative"vand "you got this" (positive)
phrase_model= glmer(gb_bool ~ gp_0 + gp_11 + gp_5 + gp_9 + gp_6 
                      + tut_count_msg_scale +
                        (1|student_id) , data=ses_full1 , family = binomial, 
                      control=glmerControl(optimizer="bobyqa"))


#MVP, phrase and macro, no name data
# Key Take away: Faster access to key learning phrases does seem to make the tutor more effective. Particularly
# macros centered around encouragment and establishing framework to learn from.
phrase_macro_model = glmer(gb_bool ~ gp_0 + gp_11 + gp_5 + gp_9 + gp_6 
                           + tut_count_msg_scale + crf_sum + crb_sum +  
                             (1|student_id) , data=ses_full1, family = binomial, 
                           control=glmerControl(optimizer="bobyqa"))

phrase_macro_modelb = glmer(gb_bool ~ gp_0 + gp_11 + gp_5 + gp_9 + gp_6 
                            + tut_count_msg_scale + crf_sum + crb_sum +  
                              (1|student_id) , data=ses_full1, family = binomial, 
                            control=glmerControl(optimizer="bobyqa"), weights = rep(10,36096))

# Looking at each students effect as a function of their session number
phrase_macro_modelc = glmer(gb_bool ~ gp_0 + gp_11 + gp_5 + gp_9 + gp_6 
                            + tut_count_msg_scale + crf_sum + crb_sum +  
                              (1+ ses_num_order_scale|student_id) , data=ses_full1, family = binomial, 
                            control=glmerControl(optimizer="bobyqa"))

#MVP with name data
# saying a students name greater than or equal to 3 times has a detremnetal effect on learning outcomes
# I suspect this is a signal of miscommunication
name_phrase_model = glmer(gb_bool ~ gp_0 + gp_11 + gp_5 + gp_9 + gp_6 
                      + tut_count_msg_scale + name_count3plus +
                        (1|student_id) , data=ses_full2 , family = binomial, 
                      control=glmerControl(optimizer="bobyqa"))


#MVP for predicting the effect of macros on session length
ses_length_model = lmer(ses_time_delta ~ crf_sum + crp_sum + crb_sum + 
                      (1|student_id) , data=ses_full1)

#MVP Student Rating
student_rating_model = lmer(student_rating ~ gb_bool + tut_count_msg_scale + crf_sum + 
                          (1|student_id) , data=ses_full1)

#g0 = hard work,
#g11 = almost there
#gp_5 = good job
#gp_9 = keep going
#gp_6 = you got this
#histogram of random effects
hist(ranef(base.model5.4)$student_id[,1])
# 95% confidence intervals
confint(ses_length_model)

#summary with coefficents
summary(base.model5.5b)

#compare each model's reletive fit with anova
anova(base.model5.5c, base.model5.5b)

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