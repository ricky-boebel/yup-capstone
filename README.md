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
    * Hard work, Working hard, You're so close, You are so close, Nice effort, You've got this, You got this, Keep at it, Keep trying, Good Job, Almost there, Yet
* Number of Questions asked (student/tutor/total)
* Question type asked (how, what, when , where , why, who)
* Length of the session
* Total Messages (student/tutor/total)

## Exploratory Data Analysis

Firstly I wanted to see what relationship my success metrics had to each other. I found an interesting relationship between student success and student satisfaction.

![Complaints by Student Success](https://github.com/ricky-boebel/yup-capstone/blob/master/images/complaint_rates.png)

Students that solved the homework problem themselves had similar satisfaction rates to those students that failed to find the solution (1.8% difference). One would expect successful students to be less likly to complain. This shows a conflict between teaching techniques and the student's needs.


To better refine a hypothesis I'm going to focus in on sessions where the student was successful. I am working under the assumption that  Within these successful lessons I'm going to look at what determines student satisfaction to better inform the interaction between teaching techniques that encourage persistence in the short term and the long term.


I focused on tutor based determinants of student success, because these are variables that are customer base would be interested in as educators.


One issue with the data was dealing with students that had different levels of usage. As the majority of students had less than 3 sessions I looked first at indicators of student success on the first session:


![Questions / Usage](https://github.com/ricky-boebel/yup-capstone/blob/master/images/blogplot1.png)

* When students participate in learning, they have successful outcomes in their session. Looking at the first 10 questions, each question asked by the student results in a 7.2% rise in success rate on that session.

This Evidence of the Yup’s Pedagogy working, especially for students willing to participate.
Informing prospective students of desired behavior before their first session.
