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

One issue with the data was dealing with students that had different levels of usage. As the majority of students had less than 3 sessions I looked first at indicators of student success on the first session:
