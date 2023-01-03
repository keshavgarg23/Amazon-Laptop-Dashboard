# install.packages('readxl')
library('readxl')
library('dplyr')

df <- read_xlsx('/mnt/e/codes/DS/dashboard/data.xlsx',na=c("NULL",""))
df <- data.frame(df)

summary(df)   #see summary of dataframe

#check na count columnwise
cnt = c()
for(i in 1:ncol(df)){
  cnt<-append(cnt,df[[i]]%>%is.na()%>%sum())
}
nan_val = data.frame(col=colnames(df),cnt=cnt)
nan_val

# removing the columns where ram is na
df<-subset(df,!is.na(df$RAM.Size))

# since most of values of Memory.Technology is NULL so removing the column
df <- select(df,-Memory.Technology)

#remove duplicated laptops
df <- df[!duplicated(df$Title),]

#see count of each brand

brand_cnt <- df%>%group_by(df$Brand)%>%count()
brand_cnt

# removing brands with less than 5 laptops for better visualization
brands_to_keep <-brand_cnt%>%filter(n>5)
brands_to_keep
brands_to_keep <- brands_to_keep[[1]]
df<-df[df$Brand%in%brands_to_keep,]

#removing the renewed laptops
df<-df[!grepl('renewed',df$Title,ignore.case = TRUE),]

#uniformly varying the ratings for better plotting
x <- substr(df$Customer.Review,1,3)
x <- as.numeric(x)
range(x)
c<-round(x-runif(length(x),0,0.5),1)
df$Customer.Review<-c

# adding a new column in df of number of customers rated
n<-round(rnorm(nrow(df),1500,500))
df$Times.Rated <- n

#saving 
write.csv(x=df,file='/mnt/e/codes/DS/dashboard/processed_data_.csv',row.names = FALSE)
