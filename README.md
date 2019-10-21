# NER-Brand-Recognition
Brand Recognition from e-commerce Product Titles 

Keras Implementation of the BiLSTM-CRF model with Glove Embedding

## Usage
1.	**Requirements**:  
    a.	Packages: Anaconda, TensorFlow, Keras   
    b.	Data: Train, Validation and Test datasets    
    c.	Glove 50B embeddings (optional) 
    
2.	**Configure Settings**:  
    a.	Change settings in model/config.py  
    b.	Main settings to change: File directories, model hyperparameters etc.  
    
3.	**Build Data**:  
    a.	Run build_data.py  
        i.	Builds embedding dictionary, text file of words, tags, as well as idx to word mapping for the model to read  
        
4.	**Train Model**:  
    a.	Run train_keras.py  
    
5.	**Test Model**:  
    a.	Run evaluate_keras.py  
    b.	Evaluates on test set. Also accepts other arguments to predict on custom string
