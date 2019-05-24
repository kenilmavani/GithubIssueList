import requests   					#import requests so we can call our API 
import json       					#json for convert the output of API in list,dictionaries
import datetime   					#it's for using datetime module for date format
from dateutil import parser 				#using parser we can change ISO format into local format 

d2 = datetime.datetime.today() - datetime.timedelta(days=6)      	# this date and time is 7 days ago date&time form current
d3 = datetime.datetime.today() - datetime.timedelta(days=1)		 # this date and time is 24 ago from current

page=1				#this is page variable for next page of issuses 
total_issues=0 			#Count of total issues in that project repository
cnt_24=0			#count of open issues that were opened in the last 24 hours
cnt_7=0				#count of open issues that were opened more than 24 hours ago but less than 7 days ago


print("Enter url:- ")
data=input()					#giving input as a link to any public GitHub repository
r = data.split('/')				#getting username and project name from input

#adding username and project name into our API 
#this api give data of all isuses which are open form that repository
#this api gave list of issus in ascending order by created date time of issuse 
url = "https://api.github.com/search/issues?q=repo:"+r[len(r)-2]+"/"+r[len(r)-1]+"+type:issue+state:open&per_page=100&page="

#loop which going to last page of issues
while True:
	url=url+str(page)       			#adding page into URL for going on next page	
	response = requests.get(url)			#getting responce from url
	data = response.text				#data came from responce
	parsed = json.loads(data)			#convert into lists,dictionaries
	total_issues=parsed["total_count"]		#getting Total issues from that dictionary
	if(len(parsed["items"])==0):			#if page is empty our while loop will break
		break
	else :													
		page+=1															#page will increase
		b=0																#it's flag for if we get any issuse which opend 7 days ago it will 1 
		for i in parsed["items"]:		
			dt = parser.parse(i["created_at"]).replace(tzinfo=None)		#we get formal date from ISO date format	
			
			if dt > d3 : 	    #comparing two dates one is from API another one is our
				cnt_24+=1   #incresing a count if issue were opened in the last 24 hours												
			elif dt > d2 :  								
				cnt_7+=1    #incresing a count if issue were opened more than 24 hours ago but less than 7 days ago
			else:														
			     b=1	#here we get first issus which opened after 7 days ago so b = 1
			     break	#we break that for loop
		if(b==1):
			break	#and also breaking our while loop too 

#total isuuses
print(" Total issues:- ",total_issues)	
#count of open issues that were opened in the last 24 hours
print(" Number of  open issues that were opened in the last 24 hours:-                             ",cnt_24) 
#count of open issues that were opened more than 24 hours ago but less than 7 days ago
print(" Number of  open issues that were  opened more than 24 hours ago but less than 7 days ago:- ",cnt_7)
#if we subtracting cnt_24 and cnt_7 from total we will get ans of last problem (issues were opened more than 7 days ago)
print(" Number of open issues that were opened more than 7 days ago:-                              ",total_issues-cnt_24-cnt_7)


