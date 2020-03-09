#Importing Dependencies
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import xgboost as xgb
from sklearn.metrics import f1_score, classification_report, accuracy_score,confusion_matrix
from sklearn.model_selection import GridSearchCV
import pickle

#Reading the file
df = pd.read_csv('concated.csv')

#Droping the unwanted columns
df.drop(['HotelRatings','HotelAddress','HotelName','Unnamed: 0','Authorlocation','AuthorName'],axis=1,inplace=True)
df.head()
#checking the null values
(df.isnull().sum(axis=0)/len(df))*100

#Droping columns with nulls with high percentage
df.drop(['Sleep Quality','Business service (e.g., internet access)','Check in / front desk'],axis=1,inplace=True)
df['Overall'] =df['Overall'].astype('str')

#Droping over all rating with null values
df.drop(df[df.Overall == '0.0'].index, inplace = True) 
df.Overall.value_counts()
df["ReviewDetails"]=df['title']+" "+df["Review"]
df.head()
#Removing Stop words and performing Stemming
stemmer = PorterStemmer()
words=stopwords.words("english")
df['cleaned'] = df['ReviewDetails'].apply(lambda x: " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower())
df['cleaned'].head()
df['Cleaned_with_price'] = df['cleaned']+" "+df['HotelPrice']
df['Cleaned_with_price'].to_pickle("cleaned.pkl")
df_cleaned=pd.read_pickle("cleaned.pkl")

# #### Splitting to test and train 
X_train, X_test, Y_train, Y_test = train_test_split(df_cleaned,df['Overall'], test_size = 0.10, random_state = 42)
#TF-IDF on Training set
vectorizer=TfidfVectorizer(min_df=0.1,stop_words="english",sublinear_tf=True,ngram_range=(1,1),norm='l2')
final_features_train = vectorizer.fit(X_train)
final_features_train = vectorizer.transform(X_train)
final_features_train.shape
#TF-IDF on Test set
final_features_test = vectorizer.transform(X_test)
final_features_test.shape

# Save the  vectorizer as a pickle string
with open('vectorizer.pk', 'wb') as fin:
    pickle.dump(vectorizer, fin)

# ## Grid Search to avoid Overfitting
RANDOM_STATE = 100
param_test = {
'max_depth':[4,5,6,10,15,20,25,30,35,50,100],
'learning_rate': [0.0001, 0.001, 0.01,0.5]
}

gsearch2 = GridSearchCV(estimator = xgb.XGBClassifier(learning_rate=0.1, n_estimators=1, max_depth=5, gamma=0, subsample=0.8, colsample_bytree=0.8,objective= 'multi:softmax', num_class = 6 ,scale_pos_weight=1), 
param_grid = param_test, scoring='accuracy', cv=5)
gsearch2.fit(final_features_train,Y_train)
gsearch2.best_params_ , gsearch2.best_score_

# # Training and testing XG Boost Model
xgb_model = xgb.XGBClassifier(max_depth=50, random_state=RANDOM_STATE,
learning_rate=0.01, colsample_bytree=.7, gamma=0, alpha=0,objective='multi:softmax', eta=0.3,subsample=0.8)
xgb_model.fit(final_features_train, Y_train)

# Save the trained model as a pickle string.
with open('model.pk', 'wb') as fin:
    saved_model = pickle.dump(xgb_model, fin)
#saved_model = pickle.dumps(xgb_model)   
# Load the pickled model 
xgb_model_from_pickle = pickle.loads(saved_model) 
xgb_prediction = xgb_model_from_pickle.predict(final_features_train)
xgb_prediction = xgb_model_from_pickle.predict(final_features_test)

## Model Evaluation
## Training Score
print('training score:', f1_score(Y_train, xgb_prediction, average='macro'))
print(classification_report(Y_train, xgb_model.predict(final_features_train)))

# Testing Score
print('validation score:', f1_score(Y_test, xgb_prediction, average='macro'))
print(classification_report(Y_test, xgb_prediction))
accuracy = accuracy_score(Y_test, xgb_prediction)
accuracy

#Confusion Matrix
confusion_matrix(Y_test, xgb_prediction)



