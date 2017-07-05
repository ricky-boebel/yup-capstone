# Initial Project Thoughts

##  Chat structure
1. Student waits for tutor matching
2. tutor is matched
3. Student waits for tutor to review problem
4. Problem Dialogue( includes images often)
5. Session ended, always student, either abrupt or expected


## Feature ideas

####  Externally Interpretable

* Session length
    * mins
    * num messages
* Usage to date
    * Interaction between usage and session length?
* Emojis used
    * By tutor
    * By student
    * Total
    * Old Emojis used?
    * Check out session 328627 (tutor using ":)" with high frequency)
* Sentiment Rating
    * Sentiment arc through session (hypothesis: negative -> positive)
* Questions asked in chat sessions?
    * num tutor ?
    * num student ?
    * total ?
    * ratio of student and tutor ?
* Num of days between chat sessions.
    * Familiarity metric that will change over time

####  Internally Interpretable

* Pictures uploaded
* Whiteboard used
* Abrupt ending
    * Bye signifier
* Opening phrase analysis
    * gender (mr, ms, mrs)
    * length
* Source of payment
    * on trial boolean
    * parent paying
    * school paying


####  Signal Isolation

* No "system alert: Student ended session" Student does not end session
    * signifier of tutor deeming a uncooperative student
* Metric for short session that may not contain signal due to student incooperation
    * i.e. gap-clarification without a student response to tutor
    * 1 or 2 student responses after session start may indicate this .
* Student is never connected
    * Check if there is ever a 'consolidated_session_category' for this instance
* Duplicate messages on the same timestamp appear on occasion, need to be removed.

## Questions for Yup

1.  Is 'consolidated_session_category' the right column to used for senior tutor rating? suspected ordering of 'consolidated_session_category'.:
    1. gap bridged
    2. gap explained
    3. gap clarification
2. Is there XXXXX number of sessions Michael indicated there were up to half a million. Just checking that there isn't more data.
3. Are there any large structural changes for:
    * tutors
        * Trainings
        * Rules
        * policies
    * Students
        * Price points (Now $69 for unlimited)
            * is there a way to tell parent paying and not parent paying
        * trial variations
        * promotions
    * both
        * Upgrades to platform


##  Secondary notes

*  What does "system warn: Tick tock. Out of minutes in 5 mins"?

*  What were the variation in pricing schemes over what time preiods?

*  Interesting gender identifier in txt ( Ms. Mr. Mrs.)

* "not quite" heavily used for wrong answers

* Do we have tutor canned responses. What are the top ones? Name exclusion?

* '*' as a typo convention

* old emojis ":/" ":)" vs new emojis

* Look at break down of "system alert", "system info", "system warn", and any others?


* A lot of hints after student uploads pic

* Can we predict un-cooperative students.

*  Does session category have to be target? If not can we focus on the engaged learner? Returning .etc

#### Checkpoint 1200 msgs into file
