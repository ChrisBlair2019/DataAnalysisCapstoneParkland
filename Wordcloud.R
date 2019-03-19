library("XML")
library(tm)
library(wordcloud)
library(SentimentAnalysis)

dataset <- read.csv(file.choose(), header = T)

datasetBBC <- subset(dataset, dataset$screen_name == "BBCBreaking")
datasetBusinessweek <- subset(dataset, dataset$screen_name == "BW")

corpus1 = VCorpus(VectorSource(datasetBBC$tweet))

corpus1

wordcloud(corpus1, max.words=100, random.order = FALSE, colors="blue")

corpus1 <- tm_map(corpus1, content_transformer(tolower))
corpus1 <- tm_map(corpus1, removeNumbers)
corpus1 <- tm_map(corpus1, removeWords, stopwords("english"))
corpus1 <- tm_map(corpus1, removeWords, c("will", "like", "says", "say"))

wordcloud(corpus1, max.words=250, random.order = FALSE, colors="blue")

corpus2 = VCorpus(VectorSource(datasetBusinessweek$tweet))

corpus2

wordcloud(corpus2, max.words=100, random.order = FALSE, colors="blue")

corpus2 <- tm_map(corpus2, content_transformer(tolower))
corpus2 <- tm_map(corpus2, removeNumbers)
corpus2 <- tm_map(corpus2, removeWords, stopwords("english"))
corpus2 <- tm_map(corpus2, removeWords, c("will", "like"))

wordcloud(corpus2, max.words=250, random.order = FALSE, colors="blue")
