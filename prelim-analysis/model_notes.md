#  Preliminary Modeling Document

###  Problem

How do we best convey the value added to student learning outcomes by Yup in a analytically-based blog post?

####  Options

1. Analysis of tutor-student interaction that shows determinants of the "growth mindset" in areas specific to Yup's chat platform?
1a. Find the determinants of the socratic learning
    a. Effect of emoji's on session category or student engagement.
    b. Using a hazard function find the determinants of growth mindset overtime? Can we find a usage threshold that yields socratic students?
        * Must find clear definition of the survival event.
        * Who do we censor?
            * Those students without an arbitrary minimum number of sessions to warrant a transition to gap-bridged. (This might be called truncation?)
            *

###  Target

* gap-bridged
    * Does it unfairly favor students that are already proficient in the subject or area?
    * Does it only measure tutor performance and not represent student success.
* Are there metrics that we can look at that have a "growth mindset" and do we see a development over time using the platform?
    * Indicators of curiosity:
        * Question asking
        * response time (median may give a better measure of engagement when not in the thinking stage)


## Model Research

####  Survival Analysis

Regardless of the target survival analysis looks like a useful way to measure on a reletively short term dataset (~12 months).

Article 1.1, Dayne Batten part 1: http://daynebatten.com/2015/02/customer-churn-survival-analysis/

* Overview of Kaplan-Meier Estimators (Prodcut Survival Estimators): https://en.wikipedia.org/wiki/Kaplan%E2%80%93Meier_estimator
    * Probabilities of churn over a period of time.
    * We can also subset the data and look at graphs of various survival curves: http://daynebatten.com/wp-content/uploads/2015/02/GenderKaplanMeier.jpeg
* Log-Rank test will yield a p-value in a single explanatory variable case.

Article 1.2, Dayne Batten part 2 multiple variables: http://daynebatten.com/2015/02/customer-churn-cox-regression/

* Cox Regression
    * Gold standard in survival analysis
    * “proportional hazards” Assumption
        * What does “proportional hazards” “proportional hazards” mean? Well, remember how we were talking about a multiplicative relationship between the baseline hazard rate and the hazard rate for a particular group? Like “coupon users churn 1.8 times faster than non-coupon users?” Yeah, well, cox regression assumes that all relationships are multiplicative throughout time. In other words, the model assumes the churn rate for coupon users is always 1.8 times higher than non-coupon users.


Article 2:, Jonathan Sedar part 1: http://blog.applied.ai/survival-analysis-part1/

* Intro idea of the hazard function
    * The hazard function λ(t)λ(t) is a related measure, telling us the probability that the event TT occurs in the next instant t+δtt+δt, given that the individual has reached timestep:
    * Could this show an increase probability of engagement/intelectual growth after a period of time using Yup?
* Survival Regression
    * Survival Regression: In the trucks example, we might want to know the relative impact of engine size, hours of service, geographical regions driven etc upon the time from first purchase to first service.
    * Cox Proportional Hazards Model
        * Having computed the survival function4 for a population, the logical next step is to understand the effects of different characteristics of the individuals. In our truck example above, we might want to know whether maintenance periods are affected more or less by mileage, or by types of roads driven, or the manufacturer, model or load-capacity of truck etc.

Article 3: donor_lifetimes_non_profit GitHub Project: https://github.com/williamtong/donor_lifetimes_non_profit

* Used a hazard function to find the most influential factors in donor churn at different periods
    * specifically the Aalen Additive model
        * For training only those donors that have left are used and then predict on donors not yet chruned
        * This model avoids the assumption of Proportional hazards.
        * Bootstrapped the model 10K times (something to consider for survey study).
    * Interpretable results that seem to be easy to explain to the public

Article 4: Aalen Additive Model Thesis:http://archimede.mat.ulaval.ca/theses/H-Cao_05.pdf

* Math Background on the model
* Gives example of drug relapse program
* Gives evaluation metric breakdown

### General

Mathcrunch rebrands to yup: https://www.inc.com/alex-moazed/edtech-startup-yup-is-taking-tutoring-to-the-next-level.html

* Provides some background on yup's rebrand to a greater focus on Socratic tutoring (https://en.wikipedia.org/wiki/Socratic_method) to better learning outcomes and loyalty.

#### Readings to-do

1. Jonathan Sedar part 2: http://blog.applied.ai/survival-analysis-part2/
