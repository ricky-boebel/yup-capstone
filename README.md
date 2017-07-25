# Texting With Socrates
#### How language effects educational outcomes?
Ricky Boebel, July 2017

## Project Description
As a data scientist looking to break into the education sector I chose to partner the [homework help application Yup](www.yup.com). Yup emphasizes a socratic learning frame work that encourages the tutor to collaborate rather than lecture.My primary focus was:

**What are the determinants of student success at Yup? How do we communicate these to customers(educators and parents)?**

## Data Overview

### Session level
There were over 40,000 unique sessions. Yup had a variety of success metrics that are worth defining:
Student success - whether the student arrived at the solution themselves. (Tutor designated)
Tutor Success - rating of the tutor. (Student designated)
Student Satisfaction - whether or not the student complained after the tutoring session.(Student designated)

### Student level

Over 2.5 million messages. Content, sent from(tutor or student) and timestamps all provided.

### Feature engineering
Feature engineering was largely dictated by creating groupings that Yup's customer base would be interested in. A key focus was on creating features that relate to the idea of fostering a [growth mindset](https://en.wikipedia.org/wiki/Mindset#Fixed_and_growth), a widely accepted psychological theory that students an be placed on a continuum according to their implicit views of "where ability comes from". Other features were focused on
* Categories defining sessions where the following growth mindset phrases appear(defined by Yup)
    * Phrase are: Hard work, Working hard, You're so close, You are so close, Nice effort, You've got this, You got this, Keep at it, Keep trying, Good Job, Almost there, and Yet
* Number of Questions asked (student/tutor/total)
* Question type asked (how, what, when , where , why, who)
* Length of the session
* Total Messages (student/tutor/total)

## Exploratory Data Analysis

Firstly I wanted to see what relationship my success metrics had to each other. I found an interesting relationship between student success and student satisfaction.

![Complaints by Student Success](https://github.com/ricky-boebel/yup-capstone/blob/master/images/complaint_rates.png)

Students that solved the homework problem themselves had similar satisfaction rates to those students that failed to find the solution (1.8% difference). One would expect successful students to be less likely to complain. This shows a conflict between teaching techniques and the student's needs.


To better refine a hypothesis I'm going to focus in on successful sessions (solution found by student). Within these successful lessons, I'm going to look at what determines student satisfaction to better inform what teaching language encourage growth in the short term but leaves the student unsatisfied in the long term.

## Mixed Effects Logistic Regression

To differentiate between student based effects and tutor based effects I used a mixed effects Logistic Regression. This model acknowledges that there is dependencies between tutoring sessions that are created by students completing multiple sessions. Accounting for these dependencies controls for noise that originates from each student having a different likelihood of satisfaction.

I focused on the effect of the tutor using any of the growth mindset phrases on student satisfaction, because these are variables that are customer base would be most compelling to educators and parents. I used a likelihood ratio test to find features that were significantly correlated with a change in student satisfaction rates. I found that the following features features had a significant effect on student satisfaction.

![Phrase Model LME](https://github.com/ricky-boebel/yup-capstone/blob/master/images/phrase_model_results.png)


## Interpretation of Effects

Duration of session (Positive effect): This is intuitive as students will be more likely to complain if they are not finding the solution quickly.
"Good job" (Positive effect): This result suggests that the phrase "good job" positively impacts the students satisfaction. Other phrases with a positive sentiment showed no effect, such as "nice effort" and "hard work". This result suggests that using the phrase "good job" is more likely to result in a satisfactory student experience than other phrases that could be used in the same context.
"Almost there" and "Yet" (Negative effect): This result refutes popular educational theory that "almost there" and "yet" encourages student percerverience and leads to improved learning outcomes. While these terms do appear in successful sessions, this result contends that students may be discouraged when tutor's use these phrases and be therefore have less sustainable learning experiences.

## Value added for Yup

My results show that there is evidence in Yup's messaging data that suggests students have an adverse reaction to being introduced to growth mindset centered techniques. Externally, there is an opportunity to communicate to yup customers that there is a need for the educational community to take a more measured gradual approach to introducing growth mindset teaching techniques and language inside and outside of the classroom. Internally, I've added value by providing information on what phrases are associated with successful and sustainable learning outcomes that could inform future tutor training.
