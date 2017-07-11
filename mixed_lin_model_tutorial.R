pitch = c(233,204,242,130,112,142)
sex = c(rep("female",3),rep("male",3))

my.df = data.frame(sex,pitch)

xmdl = lm(pitch ~ sex, my.df)
summary(xmdl)
mean(my.df[my.df$sex=="female",]$pitch)

age = c(14,23,35,48,52,67)
pitch = c(252,244,240,233,212,204)
my.df = data.frame(age,pitch)
xmdl = lm(pitch ~ age, my.df)
summary(xmdl)

install.packages(“lme4”)
library(lme4)
politeness=  read.csv("http://www.bodowinter.com/tutorial/politeness_data.csv")
!complete.cases(politeness)
boxplot(frequency ~ attitude*gender,
        col=c("white","lightgray"),politeness)

politeness.model = lmer(frequency ~ attitude +
                          (1|subject) + (1|scenario), data=politeness)
summary(politeness.model)

politeness.model = lmer(frequency ~ attitude +
                          gender + (1|subject) +
                          (1|scenario), data=politeness)


