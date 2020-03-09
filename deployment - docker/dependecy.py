import pickle
import xgboost as xgb

class dependency:
    
    def __init__(self):
        pass
    
    def vectorizer(self,filename_path):
        pickle_in = open(filename_path,"rb")
        return pickle.load(pickle_in)
    
    def prediction(self,filename_path):
        xgb_model =  open(filename_path, "rb")
        return pickle.load(xgb_model)

def give_prediction(review):
    flag=True
    depend = dependency()
    vectorizer_filename = 'E:/Models/vectorizer.pk'
    model_filename = 'E:/Models/model.pk'
    
    if flag:
      model_object=depend.prediction(model_filename)
      flag=False
      
    review_analysis=[]
    review_to_be_analyzed = review
    review_analysis.append(review_to_be_analyzed)
    vectorizers = depend.vectorizer(vectorizer_filename)
    vector_input=vectorizers.transform(review_analysis)
    predicted = model_object.predict(vector_input)
    model_object=None
    return review_to_be_analyzed,predicted[0]