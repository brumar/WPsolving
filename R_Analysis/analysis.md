Statistical analysis of the dynamic model predictions
========================================================


This analysis is the final step of a modelisation resarch programm aiming to bring quantitative support to the idea that student errors in word problem solving are not always caused by a mindless guesswork or keyword-based process but is more likely to be anchored in deep reinterpretation process occuring in case of hindrance in the solving process.

A blind algorithm generated all the possible formulas three numbers being given. The formulas are categorized according their complexity (set0 to set3 described later). P1,T1 and d are taken as token for numbers where T1>P1>d.

Another programm generated student-like solutions to some word problems describing mathematical relationships with P1,T1 and d. 
The programm mixed expert rules (computing an unknown whenever it's possible) and some reinterpretation steps to reach the solution. An example of reinterpretation step is taking "John has 4 marbles more than David" as "John has 4 marbles".
The programm was developped to generate as many solution path as possible following this pattern of expert computation rules and 1 or 2 reinterpration occuring during the solving process.

The goal is to prove that the selection of formulas generated by the second programm are more likely to occur in real world datas than blindly generated formulas. To prove that, we received datas gathered accross years by Valentine Chaillet during her Phd. More than one thousand "faulty" formulas are gathered accross 16 different problems and hundred of elementary students.

# First lines of the dataset

```r
datas = read.csv2("../CONFRONTATION_04072014_epure.csv", sep = ";", colClasses = c("factor", 
    "factor", "factor", "logical", "numeric"))
head(datas)
```

```
##   problem  set   formula selected occurrences
## 1    Tc1p set0      T1+d     TRUE           2
## 2    Tc1p set0     T1+P1    FALSE           2
## 3    Tc1p set0     T1-P1     TRUE           5
## 4    Tc1p set0      P1+d     TRUE           3
## 5    Tc1p set0      T1-d     TRUE         119
## 6    Tc1p set1 T1+(P1+d)    FALSE           0
```

Variable description :
- problem : the code name of the problem
- set : the category of formula, we chose to make categories in order to eliminate from our analysis possible heuristics related to the number of operations and the choice of operands in the solving process due to the stereotypical aspect of word problem
- formula : the formula generated by the blind algorithm
- selected : indicate if this formula is also generated by the student-like programm
- occurences : count the number of occurences in the Dataset of Valentine for this problem and this formula.


```r
Lset0 = datas$set == "set0"
Lset1 = datas$set == "set1"
Lset2 = datas$set == "set2"
Lset3 = datas$set == "set3"
Lselected = datas$selected
print("number of observations")
```

```
## [1] "number of observations"
```

```r
sum(datas$occurrences)
```

```
## [1] 1834
```


# Analysis

Binomial tests will be used to determine if there are significantly "more" occurences in the sub-selection determined by the student-like programm. Under the null hypothese the ratio of occurence in the sub-selection should follow the relative size of this selection compared to the size of the set.
Interpretation :
- The number of trial is taken as the number of occurences in the global set (set0, set1, set2, set3)
- The number of successes is the number of occurences belonging to the sub-selection determined by the programm
- The null hypothesis probability of success for each trial is the relative size of the subselection

## Binomial test for the set0 
set 0 = one operation only
(formulas like T1-d, P1+T1, etc....)


```r
numberOfFormulasInSet0 = sum(Lset0)
numberOfSelectedFormulasInSet0 = sum(Lselected & Lset0)
p_underNullHypothesis = numberOfSelectedFormulasInSet0/numberOfFormulasInSet0
numberOfOccurencesInSelectedFormulas = sum(datas$occurrences[Lselected & Lset0])
numberOfOccurences = sum(datas$occurrences[Lset0])
binom.test(numberOfOccurencesInSelectedFormulas, numberOfOccurences, p = p_underNullHypothesis, 
    alternative = "greater", conf.level = 0.95)
```

```
## 
## 	Exact binomial test
## 
## data:  numberOfOccurencesInSelectedFormulas and numberOfOccurences
## number of successes = 964, number of trials = 1031, p-value <
## 2.2e-16
## alternative hypothesis: true probability of success is greater than 0.675
## 95 percent confidence interval:
##  0.921 1.000
## sample estimates:
## probability of success 
##                  0.935
```


## Binomial test for the set1
set 1 = two operation only, no operands used twice
(formulas like (T1-d)+P1, (P1+T1)+d, etc....)


```r
numberOfFormulasInSet1 = sum(Lset1)
numberOfSelectedFormulasInSet1 = sum(Lselected & Lset1)
p_underNullHypothesis = numberOfSelectedFormulasInSet1/numberOfFormulasInSet1
numberOfOccurencesInSelectedFormulas = sum(datas$occurrences[Lselected & Lset1])
numberOfOccurences = sum(datas$occurrences[Lset1])
binom.test(numberOfOccurencesInSelectedFormulas, numberOfOccurences, p = p_underNullHypothesis, 
    alternative = "greater", conf.level = 0.95)
```

```
## 
## 	Exact binomial test
## 
## data:  numberOfOccurencesInSelectedFormulas and numberOfOccurences
## number of successes = 544, number of trials = 676, p-value <
## 2.2e-16
## alternative hypothesis: true probability of success is greater than 0.4323
## 95 percent confidence interval:
##  0.7779 1.0000
## sample estimates:
## probability of success 
##                 0.8047
```


## Binomial test for the set2 
set 2 = two operation only, one operand used twice
(formulas like (T1-d)+T1, (P1+T1)+P1, etc....)


```r
numberOfFormulasInSet2 = sum(Lset2)
numberOfSelectedFormulasInSet2 = sum(Lselected & Lset2)
p_underNullHypothesis = numberOfSelectedFormulasInSet2/numberOfFormulasInSet2
numberOfOccurencesInSelectedFormulas = sum(datas$occurrences[Lselected & Lset2])
numberOfOccurences = sum(datas$occurrences[Lset2])
binom.test(numberOfOccurencesInSelectedFormulas, numberOfOccurences, p = p_underNullHypothesis, 
    alternative = "greater", conf.level = 0.95)
```

```
## 
## 	Exact binomial test
## 
## data:  numberOfOccurencesInSelectedFormulas and numberOfOccurences
## number of successes = 15, number of trials = 69, p-value = 0.3675
## alternative hypothesis: true probability of success is greater than 0.1953
## 95 percent confidence interval:
##  0.139 1.000
## sample estimates:
## probability of success 
##                 0.2174
```


## Binomial test for the set3 
three operation only, only one operand used twice
(formulas like (T1-d)+(P1-d), (P1+T1)+(P1+d), etc....)


```r
numberOfFormulasInSet3 = sum(Lset3)
numberOfSelectedFormulasInSet3 = sum(Lselected & Lset3)
p_underNullHypothesis = numberOfSelectedFormulasInSet3/numberOfFormulasInSet3
numberOfOccurencesInSelectedFormulas = sum(datas$occurrences[Lselected & Lset3])
numberOfOccurences = sum(datas$occurrences[Lset3])
binom.test(numberOfOccurencesInSelectedFormulas, numberOfOccurences, p = p_underNullHypothesis, 
    alternative = "greater", conf.level = 0.95)
```

```
## 
## 	Exact binomial test
## 
## data:  numberOfOccurencesInSelectedFormulas and numberOfOccurences
## number of successes = 15, number of trials = 58, p-value =
## 2.651e-05
## alternative hypothesis: true probability of success is greater than 0.07763
## 95 percent confidence interval:
##  0.1667 1.0000
## sample estimates:
## probability of success 
##                 0.2586
```


# Conclusion :

There is a real difference accross the different set of formulas.
All the results are significative, unless for the **set2**. It can be caused by the lack of observations in this category, but if one compare these results to **set3** which had not many observations for a null hypothesis probability lower (get the test less powerfull), another explanation is recquired. Maybe this special use of numbers in the problem can be the footprint for a lack of commitment or mindless strategies because students did not even try to produce an answer which is - at least superficially - reliable.

Conversingly, the set which is the most important concerning the use of numbers in the text is the **set1**. Indeed, using all the number just once is a natural rule relatively to the stereotypical aspects of word problems. Unfortunately, none of the problems in the dataset could be solved this way. Students had to drop this constraint to solve this problem. But as it is a strong golden rule, it's not a surprise that our datas support the idea that strong interpretation processes occured for this problem.