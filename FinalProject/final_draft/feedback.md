# Addressing Analysis Feedback

## Additional Analysis - Connecting People #5

Completed this additional analysis using correspondance as edge weight ($W$). 

Also utilized spaCy's Named Entity Recognition (NER) to identify individuals that appear in the body of emails. The individuals are weighed less ($\frac{1}{10} W$)since there is no direct correspondance, but an inferred relationship.

## Tone of Subject #4

Changed the title from a humorous title to a passive title. While I wanted to break any tension prior to the report, I can see that it was inappropriate.

Adjusted the first two sections of the report, removing much of the passive tone such as "This analysis will focus on..." and "Without getting into too much detail...". These kind of sentences were unnecessary.

## Email Statistic Context #3

Emails chains and multiple recipients were the crux of the low email counts, though I am not willing to fix this issue. This would become a more complicated parsing issue that I was not willing to deal with. Instead, I address the issue of chain emails in the `Data Cleaning` section of the report.

## What Is Your Data? #2

I was initially unsure whether to include a section about the data. After receiving this feedback and doing peer reviews, I realized that at least a short explanation about the data, and a link to it's source, improve the readability of the analysis.

## Peer Review: Joel #1

Included a link to the source of the data, and a section that includes a description of the cleaning process and the specific data being used.

Communication frequency is interesting, but after some though I have come to the conclusion that it would require additional parsing to see improvements, such as separating emails in email chains and even more cleaning of individual names. As such, I removed this from the analysis. This visual was replaced with the distribution of email body lengths.

## Pierce Feedback

I agree that the hedging language is unnecessary and I removed much of this language.

I removed the disjointed line chart. I initially thought this would be an interesting visual, but it unfortunately requires **much** more parsing/cleaning of the data. Unfortunately, with this data being largely LLM generated, so much of the data needs cleaning and it was more than I could handle.