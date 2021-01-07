#importing all the required frameworks
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.stats import norm


# In[3]:


#reading the csv file to create the dataframe
df = pd.read_csv(r'data.csv')


# In[4]:


#replacing the spaces in column names for convenience 
df.columns
df.columns = [c.replace(' ', '_') for c in df.columns]

# understanding the names of unique tests that are given in the dataset
df['Test_Role'].unique()




# creating a dictionary with test_role as key and all of it's test_score as values (this long method was used as there were duplicate keys in df)
testScoredict = {}
for x in range(len(df)):
    currentid = df.iloc[x,1]
    currentvalue = df.iloc[x,2]
    testScoredict.setdefault(currentid, [])
    testScoredict[currentid].append(currentvalue)


# ### Consider Score Analysis

TestNames=['Test1','Test2','Test3','Test4','Test5','Test6','Test7','Test8','Test9','Test10','Test11','Test12','Test13','Test14','Test15','Test15']
Total_Questions=[50,50,50,40,45,45,45,30,70,25,50,60,35,70,40,20]  
passingScore=[35,35,35,35,35,35,35,25,65,17.5,35,42,24.5,49,28,14]
considerScore=[30,30,25,30,30,30,30,18,42,15,30,36,21,42,24,12]


#analysing number of candidates in each category as described above
cscore=[]
cscores=[]
test_taker=[]

for item in range(len(TestNames)):    
    count=0 # will represent candidates whose score is less than passingScore and greater than or equalto considerScore
    count1=0 # will represent candidates whose score is greater than or equal to  passingScore 
    count2=0  # will represent candidates whose score is less than considerScore
    for i in testScoredict[TestNames[item]]:
        if i<passingScore[item] and i>=considerScore[item]:
            count=count+1
        elif i>=passingScore[item]:
            count1=count1+1
        elif i<considerScore[item]:
            count2=count2+1
        total=count+count1
        percent= int((count*100)/total)
    
    cscore=[TestNames[item],count1,count,count+count1,count2,percent]
    cscores.append(cscore)
    candidates=count+count1+count2
    test_taker.append(candidates)

df10 = pd.DataFrame.from_records(cscores)
df10.columns =['Test_Role', '#pScoreCandidates', '#cScoreCandidates','passedCandidates','failed candidates','%cscore candidate']
df10.to_excel("cscoreAnalysis.xlsx")


# ### Percentage distribution analysis
#creating an excel file with percentage distribution of student score

result=[]
for item in range(len(TestNames)):  
    list=[]
    for i in testScoredict[TestNames[item]]: 
        popsize=len(testScoredict[TestNames[item]])
        scorePercentage=int((i*100)/Total_Questions[item])
        list.append(scorePercentage)
    datas=plt.hist(list,bins=[0, 10, 20, 30, 40, 50,60,70,80,90,100])
    new_datas = [str(round((d / popsize) * 100,2))+'%' for d in datas[0]]
    result.append(new_datas)
    
plt.clf()

df1 = pd.DataFrame.from_records(result)
df1.index =['Test1','Test2','Test3','Test4','Test5','Test6','Test7','Test8','Test9','Test10','Test11','Test12','Test13','Test14','Test15','Test15']
df1.columns =['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50-60%', '60-70%', '70-80%', '80-90%', '90-100%']
df1.to_excel("percentageDsitribution.xlsx")

#Normal Distribution Analysis 


df8 = pd.DataFrame([testScoredict])
df9=df8.T
df9.to_excel("normalDsitribution.xlsx")



#fitting the scores of each test into a normal distribution.

for j in range(len(TestNames)): 
    # Generate data
    data = testScoredict[TestNames[j]]
    n=len(data)
    # Fit a normal distribution to the data:
    mu, std = norm.fit(data)
    
    # Plot the histogram.
    data=plt.hist(data, bins=25, density=True, alpha=0.6, color='g')

    # Plot the PDF.
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = TestNames[j],"population size=",n,"Fit results: mu = %.2f,  std = %.2f" % (mu, std)
    plt.title(title)
    
    plt.show()
    
    


# ### Question Level Difficulty Analysis


#for test in range(len(TestNames)): 
df2=pd.read_csv(r'data.csv')
df2.columns = [c.replace(' ', '_') for c in df2.columns]
gf2=df2.groupby('Test_Role')

stores=[]
count=-1
for i in TestNames:
    store_y=[]
    store_n=[]
    count=count+1
    for q in range(1,Total_Questions[count]+1): 
        k='Score_'+str(q)
        yy=gf2.get_group(i)[k].replace({ 'Y' : 1, 'N' : 0 })
        y=yy.sum()
        n=(gf2.get_group(i)[k].replace({ 'Y' : 1, 'N' : 0 }).count())-y
        if n>y:
            store=[i,q,y,n]
            stores.append(store)
            
df3 = pd.DataFrame.from_records(stores)
df3.columns =['Test_Role', 'QuestionNo', 'Correct', 'Incorrect']
df3.to_excel("question_analysis.xlsx")


# ### Too long Tests Analysis



df5=pd.read_csv(r'data.csv')
df5.columns = [c.replace(' ', '_') for c in df5.columns]
gf5=df5.groupby('Test_Role')


store_blank=[]
storess=[]
count=-1
for i in TestNames: 
    count=count+1
    for q in range(1,Total_Questions[count]+1):
        k='Q'+str(q)
        score='Score_'+str(q)
        kk = gf5.get_group(i)[k].value_counts()
        blank = len(gf5.get_group(i)[k])-sum(gf5.get_group(i)[k].value_counts())
        if '0' in kk.keys():
            noResponse= kk["0"]+blank
            if ((noResponse/test_taker[count])*100)>15:
                store_blank=[i,k,noResponse,str(round(((noResponse/test_taker[count])*100),2))+'%']
                storess.append(store_blank)
df7 = pd.DataFrame.from_records(storess)
df7.columns =['Test_Role', 'QuestionNo', 'Zero responses', 'percentage of no response']
df7.to_excel("tooLongTest_analysis.xlsx")

