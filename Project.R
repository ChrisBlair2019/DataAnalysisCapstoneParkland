source("http://bioconductor.org/biocLite.R")
abiocLite("EBImage")

library(devtools)
library(ggplot2)
library(plyr)

devtools::install_github("IndicoDataSolutions/IndicoIo-R")

politicalaff = as.data.frame(FacebookAds$AdText)
politicalaff <- as.data.frame(politicalaff[!apply(is.na(politicalaff) | politicalaff == "", 1, all),])
colnames(politicalaff)[1] <- "AdText"
politicalaff <- mutate(politicalaff, "Affiliation" = "A")
politicalaff <- mutate(politicalaff, "AffililationNum" = 1)
affilation <- political(
  politicalaff[1, ]$AdText,
  api_key = '57b520f296fd011d974be811798e98f7'
)
politicalaff <- mutate(politicalaff, "AffililationObj" = list(affilation))



for (i in 1:3516){
  affilation <- political(
    politicalaff[i, ]$AdText,
    api_key = '57b520f296fd011d974be811798e98f7'
  )
  
  if(affilation$Conservative > affilation$Liberal)
  {
    politicalaff[i, ]$Affiliation = "Conservative"
  }
  else
  {
    politicalaff[i, ]$Affiliation = "Liberal" 
  }
  
  if(affilation$Conservative > affilation$Liberal)
  {
    politicalaff[i, ]$AffililationNum = affilation$Conservative 
  }
  else
  {
    politicalaff[i, ]$AffililationNum  = affilation$Liberal
  }
  
  politicalaff[i, ]$AffililationObj = list(affilation)
  
  Sys.sleep(0.1)
}

occurences<-table(unlist(politicalaff$Affiliation))
occurences


politcalaff <- mutate(politcalaff, "Liberal" = 0.0)
politcalaff <- mutate(politcalaff, "Conservative" = 0.0)


for (i in 1:3475)
{
  politcalaff[i, ]$Conservative = unlist(unlist(politcalaff[i,]$AffililationObj[[1]]$Conservative))
  politcalaff[i, ]$Liberal = unlist(unlist(politcalaff[i,]$AffililationObj[[1]]$Liberal))
}
  
# x axis lib 
# y conserv score
# color = as.factor(affiliation)
 AffiliationParty <- as.factor(politcalaff$Affiliation)
ggplot(data = politcalaff, aes(x = politcalaff$Conservative , y = politcalaff$Liberal, color = politcalaff$Affiliation)) + geom_point() + labs(title="Scatterplot of Ads targeted towards liberals and conservatives. ", y="Liberal", x="Conservative", color="Affiliation") 

ggplot(data = politcalaff, aes(politcalaff$Affiliation)) + 
  labs(title="Barplot of Affiliation", y="Number of Ads", x="Affiliation") + geom_bar()

