#  Preliminary Modeling Document

###  Problem

How do we best convey the value added by Yup in a analytical blog post?

####  Options

1. Analysis of tutor-student interaction that shows determinants of the "growth mindset" in areas specific to Yup's chat platform?
    a. Effect of emoji's on session category or student engagement.

###  Target

* Does "gap-bridged" unfairly favor students that are already proficient in the subject or area?
* Are there metrics that we can look at that have a "growth mindset" and do we see a development over time using the platform?
    * Indicators of curiosity:
        * Question asking
        * response time (median may give a better measure of engagement when not in the thinking stage)


## Model Research

####  Survival Analysis

Regardless of the target survival analysis looks like a useful way to measure on a reletively short term dataset (~12 months).

Article 1, Dayne Batten part 1: http://daynebatten.com/2015/02/customer-churn-survival-analysis/

* Overview of Kaplan-Meier Estimators (Prodcut Survival Estimators): https://en.wikipedia.org/wiki/Kaplan%E2%80%93Meier_estimator
    * Probabilities of churn over a period of time.
    * We can also subset the data and look at graphs of various survival curves: http://daynebatten.com/wp-content/uploads/2015/02/GenderKaplanMeier.jpeg
* Log-Rank test will yield a p-value in a single explanatory variable case.

Article 2:, Jonathan Sedar part 1: http://blog.applied.ai/survival-analysis-part1/

* Intro idea of the hazard function
    * The hazard function λ(t)λ(t) is a related measure, telling us the probability that the event TT occurs in the next instant t+δtt+δt, given that the individual has reached timestep:
    * Could this show an increase probability of engagement/intelectual growth after a period of time using Yup?
* Survival Regression
    * Survival Regression: In the trucks example, we might want to know the relative impact of engine size, hours of service, geographical regions driven etc upon the time from first purchase to first service.
    * Cox Proportional Hazards Model
        * Having computed the survival function4 for a population, the logical next step is to understand the effects of different characteristics of the individuals. In our truck example above, we might want to know whether maintenance periods are affected more or less by mileage, or by types of roads driven, or the manufacturer, model or load-capacity of truck etc.




#### Readings to-do

Dayne Batten part 2 multiple variables: http://daynebatten.com/2015/02/customer-churn-cox-regression/
Jonathan Sedar part 2: http://blog.applied.ai/survival-analysis-part2/
