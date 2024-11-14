import pandas as pd
import sklearn.model_selection as train_test_split
from transformers import BertTokenizer

# Load the dataset
df = pd.read_csv("generated/contracts_with_level_of_danger.csv")

# Split the dataset for the training 
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

#init token BERT 
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def preprocess_data(dataframe):
    texts = dataframe['texte_contrat'].tolist()
    labels = dataframe['niveau_danger'].tolist()
    
    # Tokenization et padding
    encoded_data = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
    
    return encoded_data, labels

# Pretrain the data and the test 
train_encodings, train_test_split = preprocess_data(train_df)
test_encodings, test_labels = preprocess_data(test_df)