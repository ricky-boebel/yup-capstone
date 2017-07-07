# Capstone Day Log

#### Day 1

* Created init_notes.md
    * Chat structure from reading chat transcripts
    * Feature ideas
        * Parsed into externally and internally Interpretable
        * Also ideas for identifying things that may skew, session_category as a target Feature
    * Yup Questions
    * Misc Notes

* Created Variable description table (session_variables.csv) for session data
    * Included questions for Yup
    * Still needs formatting to make into real table.

* Created model_notes.md
    * purpose: to better define project scope and summarize research related to model selection.

Day 2 To-Dos
1. Read ~1500 lines of messages (Most recent) and record observations.
2.  Draft email to Yup on progress and asks for Wednesday no longer than 5 questions(incorporate session_variables.csv and init_notes.md questions)
3. Create basic survival curve using section_category == 'gap-bridged' as churn proxy. Plot it.
4. Complete Reading to-dos and write up Notes
5. Clean session_variables.csv
6. Look into academic research related to language in teacher student relationship

#### Day 2

* Read 1500 lines of messages and added more observations to init_notes.md.
* Drafted email to Yup
* Read all but one of research to-dos and recorded notes in model_notes.md
* Started creating the target variable (days to first gap-bridged)


Group questions
1. Concerned that my primary variable favors students that already know the material?
2. I'm interesting in measuring what determines a students transition to a growth mindset that is indicative of (gap-clarification or gap-explained) -> gap-bridged

Day 3 To-Dos
1. Finish first survival curve
2. Review survey and Write out questions for David
3. Refine target variable (take students that have more than 5 sessions and greater than 0.8 gap-bridged)
4. Look into academic research related to language in teacher student relationship
5. Clean session_variables.csv
6. Decide on a number of sessions for cut-off.
7. Find out how many people are dropping out of gap-bridged post bridging.
8. Average time to bridge


#### Day 3

* Added columns to student level data regarding variation of days to bridged
* Added first categorical variables platform and student_platform
* Started tuning target both min sessions subset and varying x-number of gap-bridged sessions needed to qualify as gap-bridged student.
* Completed KMF with categorical variables
* Completed Nelson Aalen estimator and plotted first hazard function
* Completed 1st Aalen’s Additive model using student_platform as a categorical comparison.
* Met with David Lang and got the following takeaways: ADD AFTER MEETING

Blockers
* Concerned that subsetting is eliminating signal of some minority classes, bootstrapping from the donor lifetime study?
* Need help interpreting the cumulative hazard function to assist in the tuning process.
* Generally worried about high ratio of truncation and censorship and that I'm throwing away too much data.
* How soon should I start cross validation? Order of events looking into bootstrapping?

Day 4 To-dos:
1. Analyze the distributions
2. Add day of week and longer range seasonality/Acedemic year metrics to student data
3. Look into academic research on socratic learning (30 mins)
4. Basic NLP features (Why, What, Where, who, How), (# of '?')
5. In-depth EDA and summary to Darren


### Day 4 Summary

* Completed clear summary of EDA with markdown in an ipynb
    * Found interesting connection between gb rate and new students.
    * Also looked at different subset ranges and generally


Day 5 To-Dos
1. Narrow focus to a the areas I want to focus on for my MVP. I think its more likely to come from message data as we can make inference on how that effects learning outcomes in more understandable way.
2. Build out Language features and see if we can find linkages to gap-bridged.
3. Write up a short draft of what I've found so far for the company
4. MVP is a clean write up of my chosen narrative.

### Day 5 Summary
