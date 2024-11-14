import torch
from transformers import BertTokenizer, BertForMaskedLM, BertForSequenceClassification
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from torch.utils.data import DataLoader, TensorDataset
import os

# Load the dataset 
def load_dataset(path):
        return pd.read_csv(path)
    
# Preprocess data 
def preprocess_data(dataframe, tokenizer): 
    texts = dataframe['texte'].tolist()
    labels = [label - 1 for label in dataframe['niveau_de_danger'].tolist()]    
    encoded_data = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
    return encoded_data, labels


# train the model
def train_model(model, train_loader, num_epochs=5): 
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
    
    for epoch in range(num_epochs): 
        model.train()
        for batch in train_loader: 
            optimizer.zero_grad()
            input_ids, attention_mask, labels = [b.to(device) for b in batch]
            outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
            accuracy = (outputs.logits.argmax(dim=-1) == labels).float().mean()
            loss = outputs.loss
            loss.backward()
            optimizer.step()
        print(f'Epoch {epoch + 1}/{num_epochs}, Loss: {loss.item()}')
    print(f'Loss: {loss:.4f}, Accuracy: {accuracy:.4f}')
    

# Evaluate the model
def evaluate_model(model, test_loader): 
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    model.eval()
    predictions = []
    true_labels = []
    with torch.no_grad(): 
        for batch in test_loader: 
            input_ids, attention_mask, labels = [b.to(device) for b in batch]
            outputs = model(input_ids, attention_mask=attention_mask)
            _, predicted = torch.max(outputs.logits, dim=-1)
            predictions.extend(predicted.cpu().tolist())
            true_labels.extend(labels.cpu().tolist())
            
    return classification_report(true_labels, predictions)

#Analyze problematic section 
def analyze_problematic_sections(contract_text, danger_level): 
    return ["Section 1", "Section 2"]

# annotate the contract
def annotate_contract(model, tokenizer, contract_text): 
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    inputs = tokenizer(contract_text, padding=True, truncation=True, return_tensors='pt')
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model(**inputs)
        _, predicted = torch.max(outputs.logits, dim=-1)
        
    danger_level = predicted.item() + 1
    problematic_sections = analyze_problematic_sections(contract_text, danger_level)
    
    return {
        'danger_level': danger_level,
        'problematic_sections': problematic_sections
    }

def main():
    # load data
    df = load_dataset('./dataset/generated/contracts_with_level_of_danger.csv')
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    
    #init token BERT    
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=5)
    
    # Preprocess data 
    train_encodings, train_labels = preprocess_data(train_df, tokenizer)
    test_encodings, test_labels = preprocess_data(test_df, tokenizer)
    
    # Create dataloaders
    train_dataset = TensorDataset(train_encodings['input_ids'], train_encodings['attention_mask'], torch.tensor(train_labels))
    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
    test_dataset = TensorDataset(test_encodings['input_ids'], test_encodings['attention_mask'], torch.tensor(test_labels))
    test_loader = DataLoader(test_dataset, batch_size=8, shuffle=False)
    
    #train model 
    train_model(model, train_loader)
    
    # evaluate model 
    report = evaluate_model(model, test_loader)
    print(report)
    
    # save model
    model.save_pretrained('models/contract_model')
    
    # exemple of annotation
    contract_text = "Exemple de contrat..."
    annotation = annotate_contract(model, tokenizer, contract_text)
    print(f"Niveau de danger : {annotation['danger_level']}")
    print(f"Sections problématiques: ")
    for section in annotation["problematic_sections"]:
        print(section)

if __name__ == '__main__':
    # os.system("clear")
    main()