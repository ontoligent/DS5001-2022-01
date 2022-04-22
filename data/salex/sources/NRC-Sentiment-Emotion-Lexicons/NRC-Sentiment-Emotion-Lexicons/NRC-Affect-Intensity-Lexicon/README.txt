NRC Affect Intensity Lexicon
Version 0.5
4 May 2018
Copyright (C) 2018 National Research Council Canada (NRC)
************************************************************


************************************************************
Contact: 
************************************************************


Technical enquiries

Saif M. Mohammad (Senior Research Officer at NRC and creator of these lexicons)Saif.Mohammad@nrc-cnrc.gc.ca 

Business enquiries

Pierre Charron (Client Relationship Leader at NRC)
Pierre.Charron@nrc-cnrc.gc.ca



Information on various lexicons is available here:
http://saifmohammad.com/WebPages/lexicons.html

You may also be interested in some of the other resources and work we have done on the analysis of emotions in text:
http://saifmohammad.com/WebPages/ResearchAreas.html
http://saifmohammad.com/WebPages/ResearchInterests.html#EmotionAnalysis



************************************************************
Terms of Use: 
************************************************************

1. The lexicons mentioned in this page can be used freely for non-commercial research and educational purposes.

2. Cite the papers associated with the lexicons in your research papers and articles that make use of them. (The papers associated with each lexicon are listed below, and also in the READMEs for individual lexicons.) 

3. In news articles and online posts on work using these lexicons, cite the appropriate lexicons. For example:
"This application/product/tool makes use of the <resource name>, created by <author(s)> at the National Research Council Canada." (The creators of each lexicon are listed below. Also, if you send us an email, we will be thrilled to know about how you have used the lexicon.) If possible hyperlink to this page: http://saifmohammad.com/WebPages/lexicons.html

4. If you use a lexicon in a product or application, then acknowledge this in the 'About' page and other relevant documentation of the application by stating the name of the resource, the authors, and NRC. For example:
"This application/product/tool makes use of the <resource name>, created by <author(s)> at the National Research Council Canada." (The creators of each lexicon are listed below. Also, if you send us an email, we will be thrilled to know about how you have used the lexicon.) If possible hyperlink to this page: http://saifmohammad.com/WebPages/lexicons.html

5. Do not redistribute the data. Direct interested parties to this page: http://saifmohammad.com/WebPages/AccessResource.htm

6. If interested in commercial use of any of these lexicons, see information here: https://shop-magasin.nrc-cnrc.gc.ca/nrcb2c/app/displayApp/(cpgnum=1&layout=7.01-7_1_71_63_73_6_9_3&uiarea=3&carea=0000000104&cpgsize=0)/.do?rf=y.

7. National Research Council Canada (NRC) disclaims any responsibility for the use of the lexicons listed here and does not provide technical support. However, the contact listed above will be happy to respond to queries and clarifications.



We will be happy to hear from you, especially if:
- you give us feedback regarding these lexicons;
- you tell us how you have (or plan to) use the lexicons;
- you are interested in having us analyze your data for sentiment, emotion, and other affectual information;
- you are interested in a collaborative research project. We also regularly hire graduate students for research internships.





Creator: Saif M. Mohammad

Paper associated with this lexicon:

Word Affect Intensities. Saif M. Mohammad. In Proceedings of the 11th edition of the Language Resources and Evaluation Conference, May 2018, Miyazaki, Japan.


************************************************************
GENERAL DESCRIPTION
************************************************************

The NRC Affect Intensity Lexicon is a list of English words and their
associations with four basic emotions (anger, fear, sadness, joy). 

Words can be associated with different intensities (or degrees) of an emotion.
For example, most people will agree that the word condemn is associated with a
greater degree of anger (or more anger) than the word irritate. However,
annotating instances for fine-grained degrees of affect is a substantially more
difficult undertaking than categorical annotation: respondents are presented
with greater cognitive load and it is particularly hard to ensure consistency
(both across responses by different annotators and within the responses produced
by the same annotator). Here, for the first time, we create an affect intensity
lexicon with real-valued scores of association using best--worst scaling.

For a given word and emotion X, the scores range from 0 to 1. A score of 1 means
that the word conveys the highest amount of emotion X.  A score of 0 means that
the word conveys the lowest amount of emotion X.

The lexicon has close to 6,000 entries for four basic emotions: anger, fear,
joy, and sadness. (We will soon be adding entries for four more emotions: trust,
disgust, anticipation, and surprise. We will also be adding entries for valence,
arousal, and dominance.) It includes common English terms as well as terms
that are more prominent in social media platforms, such as Twitter. It includes
terms that are associated with emotions to various degrees. For a given emotion,
this even includes some terms that may not predominantly convey that emotion (or
that convey an antonymous emotion), and yet tend to co-occur with terms that do.
(Antonymous terms tend to co-occur with each other more often than chance, and
are particularly problematic when one uses automatic co-occurrence-based
statistical methods to capture word--emotion connotations.)



************************************************************
FILE FORMAT
************************************************************

Each line has the following format:
<Term><tab><Score><tab><AffectDimension>

<Term> is a word for which the annotations are provided;

<Score> is the real-valued emotion intensity score;

<AffectDimension> is one of the emotions (anger, fear, joy, or sadness).



************************************************************
More Information
************************************************************

Details on the process of creating the lexicon can be found in the associated paper (see above).
 
