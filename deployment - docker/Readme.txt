1)Run hoteldatacleaning.py -This file will generate a csv file containing cleaned data.
2)Run Multi-text classification using XgBoost.py - This will give the vectorizer.pkl and model.pkl which will be further used in API.
3)Please change the path of vectorizer.pkl and model.pkl in dependecy.py file.
4)Create a folder called templates and add reviewdata.html (though templates folder has been already provided.So it can be just copied and pasted)
5)Finally,run prediction.py-This will make an API call and host a user-interface where a user can add hotel review and prediction will be given.

NOTE: Model.pkl is not added as it is very big file.If model.pkl cannot be created due to any reason then you can download it from this 
link :"https://drive.google.com/open?id=1rXq3UrNbwy81MRFtMBZ-OxXY8dcAdTg9"


