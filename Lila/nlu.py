import pickle
import random
import spacy
import csv

from spacy.training.example import Example


def convert_training_csv():
    # Define the column names in the CSV file
    column_names = ['Utterance', 'Intent', 'slot_type1', 'slot_value1', 'slot_name1',
                    'slot_type2', 'slot_value2', 'slot_name2', 'slot_type3', 'slot_value3', 'slot_name3']

    # Read the CSV file and create a list of dictionaries with the data
    train_data = []
    with open('../data/intents.csv', 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, fieldnames=column_names)
        for row in csvreader:
            if row['Utterance'] == "Utterance":
                continue
            # Create a dictionary for each row
            data = (row['Utterance'], {'intent': row['Intent'], 'entities': []})

            # Extract entity information from the row
            try:
                for i in range(1, 4):
                    if row[f'slot_type{i}'] and row[f'slot_value{i}'] and row[f'slot_name{i}']:
                        entity = {
                            # 'start': row['Utterance'].index(row[f'slot_value{i}']),
                            # 'end': row['Utterance'].index(row[f'slot_value{i}']) + len(row[f'slot_value{i}']),
                            'value': row[f'slot_value{i}'],
                            'entity': row[f'slot_type{i}'],
                            'slot_name': row[f'slot_name{i}']
                        }
                        data[1]['entities'].append(entity)

                # Add the row data to the list of training data
                train_data.append(data)
            except ValueError as ex:
                print("Error:", ex)
                print(row)
                input("Continue?")
                continue

    with open('../data/intents_list.pickle', 'wb') as f:
        pickle.dump(train_data, f)

    return train_data



def train_nlu():
    # define the training data set with examples of text and their corresponding intents and entities
    with open('../data/intents_list.pickle', 'rb') as f:
        # load the object from the file
        TRAIN_DATA = pickle.load(f)

    # create a blank English NLP object
    nlp = spacy.blank("en")

    # create the TextCategorizer component to classify intents
    textcat = nlp.add_pipe("textcat")
    textcat.add_label("buy_laptop")
    textcat.add_label("weather")

    # create the EntityRecognizer component to detect entities
    ner = nlp.add_pipe("ner")
    ner.add_label("product")
    print(TRAIN_DATA[0])

    # train the NLU model
    optimizer = nlp.begin_training()
    for i in range(10):
        random.shuffle(TRAIN_DATA)
        for text, annotations in TRAIN_DATA:

            # ATTEMPT 2
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], sgd=optimizer)

            # ATTEMPT 1
            # doc = nlp.make_doc(text)
            # doc.cats = annotations["intent"]
            #
            # # visibility output
            # print("text:", text)
            # print("intent:", annotations["intent"])
            # print("entities", annotations["entities"])
            # input("pls stop")
            #
            # for entity in annotations["entities"]:
            #     ent_label, ent_text, ent_name = entity.items()
            #     print("doc", doc.ents)
            #     print("new", [(ent_label, ent_text)])
            #     doc.ents = list(doc.ents) + [(ent_label, ent_text)]
            #
            # example = (doc, doc.cats)
            # nlp.update([example])

    return nlp


def run_nlu():
    # train a model
    nlp = train_nlu()

    # test the model on some input text
    check_doc = nlp("I want to buy a new phone")
    print(check_doc.cats)
    for entity in check_doc.ents:
        print(entity.text, entity.label_)



# reformat and save training data
convert_training_csv()

# do nlp stuff
run_nlu()
