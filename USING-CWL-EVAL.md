
# CWL Eval vs. TREC Eval 

Below we provide a short tutorial on running `cwl-eval` and some of the differences to `trec_eval`. 

## Results and Judgements

Imagine that we have a result file (called `test.res`) in TREC format that contains the following ranking for topic T1 by system R1. 
The six-columns represent: topic, dummy, docid, rank, score, and run name. 

   |   |    |     |     |      |    |
   |---|----|-----|-----|------|----|
   |T1 | E2 | D13 |   1 |  4.3 | R1 |
   |T1 | E2 | D22 |   2 |  4.2 | R1 |
   |T1 | E1 | D43 |   3 |  4.1 | R1 |
   |T1 | E2 | D47 |   4 |  3.9 | R1 |
   |T1 | E3 | D52 |   5 |  3.8 | R1 |
   |T1 | E1 | D65 |   6 |  3.7 | R1 |
   |T1 | E2 | D72 |   7 |  3.6 | R1 |
   |T1 | E1 | D89 |   8 |  3.5 | R1 |
   |T1 | E2 | D91 |   9 |  3.4 | R1 |
   |T1 | E3 | D10 |  10 |  3.3 | R1 |



Now imagine we have a QREL file (called `test.qrel`) in TREC Format that contains the corresponding judgements for T1.
The four-columns represent: topic, dummy, docid, and judgement. Here the judgements are binary.

   |    |     |     |    |
   |----|-----|-----|----|
   | T1 |  00 | D13 |  1 |
   | T1 |  00 | D22 |  0 |
   | T1 |  00 | D43 |  1 |
   | T1 |  00 | D47 |  1 |
   | T1 |  00 | D52 |  0 |
   | T1 |  00 | D65 |  0 |
   | T1 |  00 | D72 |  1 |
   | T1 |  00 | D89 |  0 |
   | T1 |  00 | D91 |  1 |
   | T1 |  00 | D10 |  0 |
 

# Using `cwl-eval` to compute specific metrics

Let's say we are interested in reporting the Precision at 10, the Average Precision, and the nDCG@10.

To do this specifically with `cwl-eval`, we need to create a metrics file (lets call it,  `test.metrics`) and add the metrics we would like it to calculate, e.g.:

    PrecisionCWLMetric(10)
    NDCGCWLMetric(10)
    APCWLMetric()

and then run:

    cwl-eval test.qrels test.res -m test.metrics


This will produce the following rows reporting each measurement for each topic (here we only have one topic).
The columns represent: topic, measure, expected utility, expected total utility, expected cost, expected total cost, and expected depth.
    
   |       |           |       |           |           |           |        |
   |-------|-----------|-------|-----------|-----------|-----------|--------|
   | T1	| P@10	    | 0.50	| 5.0000	| 1.0000	| 10.000	| 10.000 |
   | T1	| NDCG-k@10	| 0.56	| 2.5650	| 1.0000	| 4.5436	| 4.5436 |
   | T1	| AP	    | 0.71	| 1.9287	| 1.0000	| 2.7214	| 2.7214 |

Note that `cwl-eval` doesnt just provide one measurement, it produces a series of measurements for each metric. 
Also, note that the expected depth and expected cost are equal, because by default the cost of inspecting an item is 1.
Later we will show an example where the costs are different.



# Differences with trec_eval

So how does this relate to trec_eval??

If we run trev_eval:

    trec_eval test.qrels test.res -m all_trec -q | grep "T1"

Then we obtain the following ouput for topic T1 - where the columns denote the measure, topic, and measurement.


|                           |       |      |
|---------------------------|-------|------|
| num_ret               	| T1	| 10   | 
| num_rel               	| T1	| 5    | 
| num_rel_ret           	| T1	| 5    | 
| map                   	| T1	| 0.71 | 
|                           |       |      | 
|  ...                      |       |      | 
|                           |       |      | 
| P_10                  	| T1	| 0.50 |
|                           |       |      | 
|  ...                      |       |      | 
|                           |       |      | 
| ndcg_cut_10           	| T1	| 0.87 |
|                           |       |      | 
|  ...                      |       |      | 
|                           |       |      | 




## Comparing Measurements
First, `trec_eval` produces only one measurement per metric. Sometimes the measurement will be a count, i.e. number of retrieved items (num_ret),
 sometimes it will be an expected utility i.e. for average precision (map), and precision at 10 (P_10), and sometimes a normalized score i.e. ndcg.

This means that metrics in `trec_eval` CAN NOT BE DIRECTLY compared. i.e. it doesn't make sense to say the `ndcg` is higher than the `map`.


This is a fundamental difference. In `cwl-eval` all measurements in a given column are of the same type with the same units. 
So given our example topic, we have assumed that a document is either relevant or not, and thus gives a gain 1 or 0. This means that
the expected utility is in terms of: gain per doc. and the expected total utility is the total gain, and expected depth is in docs. 

This means that all metrics in `cwl-eval` CAN BE DIRECTLY compared. i.e. we can say that under `AP` the expected utility is higher than under `NDCG`.


### Precision and Average Precision

As it happens precision and average precision are expected utilities. Thus, both `trec_eval` and `cwl-eval` report the same values. i.e. 0.5 and 0.71 respectively.


### Discounted Cumulative Gain

However, for Normalized Discounted Cumuluative (NDCG) the score is not an expected utility. And so `trec_eval` reports 0.87 as per the implementation of the metric in the original paper [cite].

In `cwl-eval` the discount function used in NDCG is scaled, to represent a probability distribution representing the weight associated with each item at position i.
This scaling means that `cwl-eval` reports the expected utility given the user browsing model defined by NDCG - this is 0.56.

By doing so, we are now able to directly compare the expected utilities of each of the different metrics. Thus, `cwl-eval` tells us that, 
the expected utility under `AP` is higher than the expected utility under `ndcg-k=10'. In this case, acting according to the user browsing model underlying 
`AP` would result in a higher rate of gain! But would it mean that the user inspects more or less items? 
Or does it imply that the user would get higher or lower total gain?



## Related Measurements
A key difference is that `cwl-eval` tells us more than just the expected utility. 


Expected Utility (EU) is essentially the rate of gain (gain/doc) - i.e. how much a user would expect to get per item. This is like velocity (10km/hr).
But it does not tell us for how long.


Expected Depth (ED) is how many items a user is expected to examine (docs). This is like time (hrs).


Expected Total Utility (ETU) is how much gain we expect the user to accumuluted. This is like the total distance traveled.


Much like how distance = velocity * time, the EU, ED and ETU are related:

    ETU = EU * ED


Taken together we can then say the following about the performance on topic T1:

Under `P@10`, EU = 0.5, and ED=10, so ETU = 0.5 * 10 = 5. 
Or in words, the rate of encountering relevant items is 1/2, and we expect the user to examine 10 items, 
so we would expect the user to find 5 relevant items in total.

Under `NDCG-k@10`, EU = 0.5645, and ED=4.5436, so ETU = 2.565. 
Or in words, the rate of encountering relevant items is 0.5645, and we expect the user to examine 4.5436 items, 
so we would expect the user to find 2.565 relevant items in total.

Under `AP`, EU = 0.7087, and ED=2.7214, so ETU = 1.9287. 
Or in words, the rate of encountering relevant items is 0.7087, and we expect the user to examine 2.7214 items, 
so we would expect the user to find 1.9287 relevant items in total.

As we can see, the different metrics, which encode different user browsing models, tells us very different stories
 about how the user will behave and how much relevance (gain) they will receive, and at what rate. 

So if we are interested in how much relevance (gain) they will accrue -- then ETU is of interest -- 
if we care about the rate at which they get that relevance (gain) then EU is of interest. 


## Costs

The next major difference between `cwl-eval` and `trec-eval` is that `cwl-eval` lets you also calculate the cost of interacting
with the result list. By default, if no costs are included, `cwl-eval` assumes that each item costs 1 unit of cost - with no units specified.

However, different items take longer or shorter amounts of time to process and consume 
- for example, a long document vs a short document, a image result summary vs a entity card.

`cwl-eval` lets you specific the cost associated with each item. 

More details on cost to be added.
