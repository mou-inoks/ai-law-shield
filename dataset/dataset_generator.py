import pandas as pd
import random
import os

# Function to generate clauses of contracts
def generate_contract(id_contract):
    clauses = [
        "Le client devra payer 10 000 € dans les 30 jours suivant la signature.",
        "Le fournisseur peut résilier le contrat sans préavis en cas de non-paiement.",
        "Le client accepte que toutes ses données personnelles soient partagées avec des partenaires tiers.",
        "Le fournisseur peut modifier unilatéralement les termes du contrat à tout moment.",
        "Le contrat stipule que l'utilisateur cède tous ses droits d'auteur au fournisseur.",
        "Le fournisseur pourra installer un logiciel de surveillance sur les appareils de l'utilisateur.",
        "L'utilisateur autorise le suivi de son activité en ligne sans restriction pendant la durée du contrat.",
        "Le fournisseur se réserve le droit de collecter toutes les données bancaires de l'utilisateur.",
        "L'utilisateur doit payer des frais supplémentaires en cas de retard dans le paiement sans possibilité de contestation."
    ]
    
    # Choose wich clause randomly to create a text with the contract
    contract_text = " ".join(random.sample(clauses, random.randint(3, 6)))
    
    # Level of danger and annotation level
    level_of_danger = random.randint(1, 5)
    
    
    annotations = []
    
    if level_of_danger == 1:
        annotations = []
    elif level_of_danger == 2:
        annotations = [
            {"partie": "Le fournisseur peut résilier le contrat sans préavis en cas de non-paiement.",
             "justification": "Clause qui pourrait désavantager l'utilisateur en cas de problème de paiement, mais généralement acceptable."},
            {"partie": "L'utilisateur doit payer des frais supplémentaires en cas de retard.",
             "justification": "Les frais supplémentaires sont un peu excessifs mais pas nécessairement dangereux."}
        ]
    elif level_of_danger == 3:
        annotations = [
            {"partie": "Le contrat stipule que l'utilisateur cède tous ses droits d'auteur au fournisseur.",
             "justification": "Cession complète des droits d'auteur, ce qui peut nuire à l'utilisateur en cas de création d'œuvres originales."},
            {"partie": "L'utilisateur autorise le suivi de son activité en ligne sans restriction.",
             "justification": "Suivi intrusif de l'activité en ligne de l'utilisateur sans limitations."}
        ]
    elif level_of_danger == 4:
        annotations = [
            {"partie": "Le fournisseur pourra installer un logiciel de surveillance sur les appareils de l'utilisateur.",
             "justification": "Installation de logiciels de surveillance sur les appareils personnels, ce qui est très intrusif et risqué."},
            {"partie": "Le fournisseur se réserve le droit de collecter toutes les données bancaires de l'utilisateur.",
             "justification": "Collecte de données bancaires sans restriction, ce qui présente un grave risque pour la sécurité financière de l'utilisateur."}
        ]
    else:
        annotations = [
            {"partie": "Le fournisseur se réserve le droit de collecter toutes les données bancaires de l'utilisateur.",
             "justification": "Collecte illimitée des informations financières personnelles, ce qui constitue une grave menace pour la sécurité."},
            {"partie": "Le fournisseur peut modifier unilatéralement les termes du contrat à tout moment.",
             "justification": "Modification unilatérale des conditions du contrat, sans possibilité de recours pour l'utilisateur, ce qui est abusif."},
            {"partie": "L'utilisateur autorise le suivi de son activité en ligne sans restriction pendant la durée du contrat.",
             "justification": "Suivi intrusif et surveillance continue, nuisant à la liberté et à la vie privée de l'utilisateur."}
        ]
    
    return {
        "id_contrat": id_contract,
        "texte": contract_text,
        "niveau_de_danger": level_of_danger,
        "annotation": annotations
    }

# Create a list of 150 contracts 
contracts = [generate_contract(i) for i in range(1, 151)]

# Convert into Dataframe pandas 
df = pd.DataFrame(contracts)


os.makedirs('generated', exist_ok=True)

df.to_csv("generated/contracts_with_level_of_danger.csv", index=False)
