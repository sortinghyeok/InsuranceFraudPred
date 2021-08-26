#!/usr/bin/env python
# coding: utf-8

# ## 시각화 및 데이터 분석
# 
# 2021.08.25(수)

# #### 모듈 설치 (이미 설치 되어있는 경우 생략)

# In[1]:


pip install scikit-learn


# In[2]:


pip install scipy


# In[3]:


pip install numpy


# In[4]:


pip install pandas


# In[5]:


pip install matplotlib


# #### 샘플링 모듈 (일반)

# In[6]:


pip install -U imbalanced-learn


# #### 샘플링 모듈 (anaconda)

# In[7]:


conda install -c conda-forge imbalanced-learn


# In[ ]:





#  

# In[8]:


from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt


# In[9]:


# import random undersampling and other necessary libraries 
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# In[10]:


import pandas as pd
df = pd.read_csv("insurancedata.csv")
print(df.shape)
print(df.head())


# ## N : 0 / Y : 1 의 각각 비율 확인

# In[11]:


df.SIU_CUST_YN.value_counts()


# In[12]:


df.SIU_CUST_YN.value_counts(normalize=True).plot(kind='bar', color = "black")
print(df.SIU_CUST_YN.value_counts(normalize=True)*100)


# ## 데이터 추가정제
# 
# 데이터에 맞춰서 하나만 실행

# In[13]:


#insurance data

df['SIU_CUST_YN'].replace('N', 0, inplace = True)
df['SIU_CUST_YN'].replace('Y', 1, inplace = True)
df['FP_CAREER'].replace('N', 0, inplace = True)
df['FP_CAREER'].replace('Y', 1, inplace = True)
df.drop(['Unnamed: 0'], axis=1, inplace = True)
df.drop(['EXPR_SUM'], axis=1, inplace = True)
df.drop(['TOTALPREM'], axis=1, inplace = True)


# In[14]:


df.head()


# In[15]:


X = df.iloc[:,1:] # SIU_CUST_YN을 제외한 모든 cloumn
y = df.iloc[:,0] # SIU_CUST_YN


# In[16]:


# 데이터에 StartifiedKFold를 적용하기 위해서 nd.array형태로 데이터 변환
X = X.to_numpy()
print(type(X))


# In[17]:


from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold

from collections import Counter
from imblearn.over_sampling import SVMSMOTE
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import confusion_matrix, accuracy_score,precision_score,recall_score,f1_score

model = LogisticRegression()

SK_fold = StratifiedKFold(n_splits=4)
print(SK_fold.get_n_splits(df, df['SIU_CUST_YN']))

result_data = []
answers=[]
result_y = []


accuracy = []
precision = []
recall = []
fscore = []
train_idx = []
test_idx = []

for train_index, test_index in SK_fold.split(X,y):
    print("TRAIN:", train_index, "TEST:", test_index)
    train_idx.append(train_index)
    test_idx.append(test_index)
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    
    #SVMSOMTE -> 오버샘플링 기법
    SVMSOMTE = SVMSMOTE()
    X_train_SVMSOMTE, y_train_SVMSOMTE = SVMSOMTE.fit_resample(X_train, y_train)
    
    print("Before Sampling: ",Counter(y_train))
    print("After oversampling(ADASYN): ",Counter(y_train_SVMSOMTE))
    
    # 해당 변수를 설정해서 Sampling 방식 선택 후 머신러닝 실행
    X_train_sampling = X_train_SVMSOMTE
    y_train_sampling = y_train_SVMSOMTE
    
    scaler = StandardScaler()
    X_train_sampling = scaler.fit_transform(X_train_sampling)
    X_test = scaler.transform(X_test)
    
    # 학습 알고리즘 예시 (LogisticRegressiong - 로지스틱 회귀분석)
    model.fit(X_train_sampling, y_train_sampling)
    
    # sklearn에서 제공하는 score값
    print('score =', model.score(X_test, y_test))
    
    # 각 속성별 가중치 -> 절대값으로 보면됨.
    print('coef =', model.coef_)
    
    print('x_result =', model.predict_proba(X_test))
    
    
    result_data.append(model.predict_proba(X_test)[:,1:])
    answers.append(y_test)
    
    predict_X = model.predict(X_test)
    result_y.append(model.predict(X_test))
    
    print('result')
    print("---------------------------")
    print('accuracy: %.2f' % accuracy_score(y_test, predict_X))
    print('precision: %.2f' % precision_score(y_test, predict_X))
    print('recall: %.2f' % recall_score(y_test, predict_X))
    print('F1: %.2f' % f1_score(y_test, predict_X))
    
    
    accuracy.append(accuracy_score(y_test, predict_X))
    precision.append(precision_score(y_test, predict_X))
    recall.append(recall_score(y_test, predict_X))
    fscore.append(f1_score(y_test, predict_X))
    
    import seaborn as sns
    confusion = confusion_matrix(y_true = y_test
                             , y_pred = predict_X)

    plt.figure(figsize=(6, 5))
    sns.heatmap(confusion, annot=True, annot_kws={'size':15}, cmap='OrRd', fmt='.10g')
    plt.title('Confusion Matrix')
    plt.show()


# ## 교차검증 평균 값

# In[18]:


import itertools
answers = list(itertools.chain.from_iterable(answers))
result_y = list(itertools.chain.from_iterable(result_y))


# In[19]:


confusion = confusion_matrix(y_true = result_y
                             , y_pred = answers)


# In[20]:


plt.figure(figsize=(6, 5))
sns.heatmap(confusion, annot=True, annot_kws={'size':15}, cmap='OrRd', fmt='.10g')
plt.title('Confusion Matrix')
plt.show()


# In[21]:


print('mean')
print("---------------------------")
print('accuracy: %.2f' % (sum(accuracy)/len(accuracy)))
print('precision: %.2f' % (sum(precision)/len(precision)))
print('recall: %.2f' % (sum(recall)/len(recall)))
print('F1: %.2f' % (sum(fscore)/len(fscore)))


# ## 데이터 확인 및 정제

# In[22]:


result_data = list(itertools.chain.from_iterable(result_data))
result_data = list(map(float, result_data))


# In[23]:


# datas => 정답여부 
# test_idx => test_index의 index number
# answers => y_test(정답)
# result_data => train 후 test_X를 활용해 예측된 결과값

datas = []
for i in range(len(answers)):
    if answers[i] == 1:
        if result_data[i] >=0.5:
            datas.append(1)
        else :
            datas.append(0)
            
    elif answers[i] == 0:
        if result_data[i] <0.5:
            datas.append(1)
        else :
            datas.append(0)
        


# In[24]:


status = []
for i in range(len(answers)):
    if result_data[i] <0.5:
        status.append('주의')
    elif result_data[i] <0.7:
        status.append('경계')
    else:
        status.append('위험')
            


# In[25]:


print(len(answers), len(result_data), len(datas), len(status))


# In[26]:


print(type(answers), type(answers[0]))
print(type(result_data), type(result_data[0]))
print(type(datas), type(datas[0]))
print(type(status), type(status[0]))


# In[27]:


df_result = pd.DataFrame({'answers':answers,'result_data':result_data,'datas':datas, 'status':status})


# In[28]:


df_result
# column 조치사항 result_data(예측 확률) 기준'주의'(0.0~0.5),'경계'(0.5~0.7),'위험'(0,7~1.0)


# 실제 데이터에서는 answer(정답), datas(정답유무)를 제외하고    
# result_data(사기꾼일 확률)과 status(주의정도)를 붙이는 형태로 결과도출

# In[29]:


result_csv = df.join(df_result)
result_csv


# In[30]:


result_csv.to_csv('result.csv')


# ## 결과 데이터 정제

# In[31]:


y1 = np.array([0 for i in range(10)])
# result_data(예측된 확률값)을 기준으로 0~0.1/0.1~0.2/0.2~0.3/.../0.9~1.0으로 총 10가지로 분류
# datas(정답여부)를 기준으로 정답인 데이터들만 추가함. 
count = 0
for i in df_result['datas']:
    if i==1 and df_result['result_data'][count] < 0.1 :
        y1[0] +=1
    elif i==1 and df_result['result_data'][count] < 0.2 :
        y1[1] +=1
    elif i==1 and df_result['result_data'][count] < 0.3 :
        y1[2] +=1
    elif i==1 and df_result['result_data'][count] < 0.4 :
        y1[3] +=1
    elif i==1 and df_result['result_data'][count] < 0.5 :
        y1[4] +=1
    elif i==1 and df_result['result_data'][count] < 0.6 :
        y1[5] +=1
    elif i==1 and df_result['result_data'][count] < 0.7 :
        y1[6] +=1
    elif i==1 and df_result['result_data'][count] < 0.8 :
        y1[7] +=1
    elif i==1 and df_result['result_data'][count] < 0.9 :
        y1[8] +=1
    elif i==1 and df_result['result_data'][count] <= 1 :
        y1[9] +=1
    count+=1


# In[32]:


y3 = np.array([0 for i in range(10)])
# result_data(예측된 확률값)을 기준으로 0~0.1/0.1~0.2/0.2~0.3/.../0.9~1.0으로 총 10가지로 분류
# datas(정답여부)를 기준으로 오답인 데이터들만 추가함. 
count = 0
for i in df_result['datas']:
    if i==0 and df_result['result_data'][count] < 0.1 :
        y3[0] +=1
    elif i==0 and df_result['result_data'][count] < 0.2 :
        y3[1] +=1
    elif i==0 and df_result['result_data'][count] < 0.3 :
        y3[2] +=1
    elif i==0 and df_result['result_data'][count] < 0.4 :
        y3[3] +=1
    elif i==0 and df_result['result_data'][count] < 0.5 :
        y3[4] +=1
    elif i==0 and df_result['result_data'][count] < 0.6 :
        y3[5] +=1
    elif i==0 and df_result['result_data'][count] < 0.7 :
        y3[6] +=1
    elif i==0 and df_result['result_data'][count] < 0.8 :
        y3[7] +=1
    elif i==0 and df_result['result_data'][count] < 0.9 :
        y3[8] +=1
    elif i==0 and df_result['result_data'][count] <= 1 :
        y3[9] +=1
    count+=1


# In[33]:


y2 =  np.array([0 for i in range(10)])
# result_data(예측된 확률값)을 기준으로 0~0.1/0.1~0.2/0.2~0.3/.../0.9~1.0으로 총 10가지로 분류
# datas(정답여부)와 상관없이 모든 데이터를 추가함 
for count in range(len(df_result['result_data'])):
    if df_result['result_data'][count] < 0.1 :
        y2[0] +=1
    elif df_result['result_data'][count] < 0.2 :
        y2[1] +=1
    elif df_result['result_data'][count] < 0.3 :
        y2[2] +=1
    elif df_result['result_data'][count] < 0.4 :
        y2[3]+=1
    elif df_result['result_data'][count] < 0.5 :
        y2[4] +=1
    elif df_result['result_data'][count] < 0.6 :
        y2[5] +=1
    elif df_result['result_data'][count] < 0.7 :
        y2[6] +=1
    elif df_result['result_data'][count] < 0.8 :
        y2[7] +=1
    elif df_result['result_data'][count] < 0.9 :
        y2[8] +=1
    elif df_result['result_data'][count] <= 1:
        y2[9] +=1


# In[34]:


df = pd.DataFrame({'correct':y1,'all':y2,'wrong':y3})
# 정답, 전체, 오답 순


# In[35]:


print(df)


# ## 데이터 시각화

# In[36]:


x =  np.array([i for i in range(10)])


# In[37]:


# 예측한 전체 데이터 갯수

tick_size = 13 ## 눈금 폰트 사이즈
axis_label_size = 15 ## x축, y축 폰트 사이즈

fig = plt.figure(figsize=(10,10)) ## Figure 생성 사이즈는 10 by 10
ax = fig.add_subplot() ## Axes 추가
bars = plt.bar(x,y2, width=0.5, color = 'orange')
plt.xlabel('result')
plt.ylabel('count')

for i, b in enumerate(bars):
    ax.text(b.get_x()+b.get_width()*(1/2),b.get_height()+0.1,                 y2[i],ha='center',fontsize=13)
xtick_label_position = list(range(len(x)))
plt.xticks(xtick_label_position, x, fontsize=tick_size)

plt.show()


# In[38]:


# 정답 갯수

tick_size = 13 ## 눈금 폰트 사이즈
axis_label_size = 15 ## x축, y축 폰트 사이즈

fig = plt.figure(figsize=(10,10)) ## Figure 생성 사이즈는 10 by 10
ax = fig.add_subplot() ## Axes 추가
bars = plt.bar(x,y1, width=0.5, color ='green')
plt.xlabel('result')
plt.ylabel('count')

for i, b in enumerate(bars):
    ax.text(b.get_x()+b.get_width()*(1/2),b.get_height()+0.1,                 y1[i],ha='center',fontsize=13)
xtick_label_position = list(range(len(x)))
plt.xticks(xtick_label_position, x, fontsize=tick_size)

plt.show()


# In[39]:


# 오답 갯수

tick_size = 13 ## 눈금 폰트 사이즈
axis_label_size = 15 ## x축, y축 폰트 사이즈

fig = plt.figure(figsize=(10,10)) ## Figure 생성 사이즈는 10 by 10
ax = fig.add_subplot() ## Axes 추가
bars = plt.bar(x,y3, width=0.5, color ='blue')
plt.xlabel('result')
plt.ylabel('count')

for i, b in enumerate(bars):
    ax.text(b.get_x()+b.get_width()*(1/2),b.get_height()+0.1,                 y3[i],ha='center',fontsize=13)
xtick_label_position = list(range(len(x)))
plt.xticks(xtick_label_position, x, fontsize=tick_size)

plt.show()


# In[40]:


import matplotlib.pyplot as plt
# 주황으로 보이는 부분(+숫자)이 오답이라고 생각하면 됨.

tick_size = 13 ## 눈금 폰트 사이즈
axis_label_size = 15 ## x축, y축 폰트 사이즈

fig = plt.figure(figsize=(10,10)) ## Figure 생성 사이즈는 10 by 10
ax = fig.add_subplot() ## Axes 추가
bars = plt.bar(x,y2, width=0.5, color = 'orange')
bars2 = plt.bar(x,y1, width=0.5, color ='green')
plt.xlabel('result')
plt.ylabel('count')

for i, b in enumerate(bars2):
    ax.text(b.get_x()+b.get_width()*(1/2),b.get_height()+0.1,                 y2[i]-y1[i],ha='center',fontsize=13)
    
xtick_label_position = list(range(len(x)))
plt.xticks(xtick_label_position, x, fontsize=tick_size)

plt.show()


# In[41]:


import matplotlib.pyplot as plt
from matplotlib import rc
get_ipython().run_line_magic('matplotlib', 'inline')
rc('font', family='AppleGothic')

# 주황으로 보이는 부분이 오답이라고 생각하면 됨.
bins = np.arange(4) - 0.5
ys, xs, patches = plt.hist(df_result['status'], color = 'black',bins=bins, rwidth=0.4,)
for i in range(0, len(ys)):
    ## 앞에서 plt.hist 가 리턴하는 값이 bar의 x, y좌표이기 때문에 
    ## 이 값을 이용해서 글자를 어디에 넣을지 결정해줌. 
    plt.text(x=xs[i]+0.35, y=ys[i]+0.015, 
             s='{:0>4.1f}%'.format(ys[i]/len(df_result)*100), ## 넣을 스트링
             fontsize=10,## 크기 
             color='black',)
plt.xlabel('result')
plt.xticks(['주의','경계','위험'])
plt.ylabel('count')
plt.show()


# In[ ]:




