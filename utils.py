import csv
import yaml

from Lila import config
from Lila.config import *


def save_interactions():
    error_count = 0

    # Open the log file for reading
    with open(log, 'r') as logged:
        # Create a CSV file for writing
        with open(log_file, 'w', newline='') as csv_file:
            # Create a CSV writer object
            writer = csv.writer(csv_file)

            # Write the header row
            writer.writerow(['Date', 'Time', 'Milli', 'Level', 'Message'])

            # Read each line from the log file and write it to the CSV file
            message = ''
            for line in logged:
                try:
                    # Check if the line contains '&'
                    if '&' in line:
                        # If it does, split the line into its components
                        message_parts = line.strip().split(' & ')

                        # Extract the timestamp, level, and message from the message parts
                        timestamp, milli = message_parts[0].split(',')
                        date, time = timestamp.split(' ')
                        level = message_parts[1]
                        message = message_parts[2]
                    else:
                        # If it doesn't, append the line to the message of the previous row
                        message += line.strip()

                    # Write the components to the CSV file
                    writer.writerow([date, time, milli, level, message])
                except Exception:
                    error_count += 1
    print(f"Error count while saving log file: {error_count}")


def show_session():
    with open(log, 'r') as file:
        contents = file.read()
        print(contents)


def csv_to_yaml(csv_file_path):
    yaml_file_path = config.yaml_file_path

    data = {"nlu": []}

    with open(csv_file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            intent = row["Intent"]
            example = row["Utterance"]
            entities = []
            for i in range(1, 4):
                entity = row[f"Entity{i}"]
                value = row[f"Value{i}"]
                if entity and value:
                    entities.append(f"[{value}]({entity})")
            if entities:
                example_with_entities = example + " " + " ".join(entities)
            else:
                example_with_entities = example

            found_intent = False
            for intent_data in data["nlu"]:
                if intent_data["intent"] == intent:
                    intent_data["examples"].append(example_with_entities)
                    found_intent = True
                    break

            if not found_intent:
                data["nlu"].append({"intent": intent, "examples": [example_with_entities]})

    with open(yaml_file_path, "w") as file:
        yaml.dump(data, file)


def csv_to_yaml2(csv_file):
    yaml_file = config.yaml_file_path

    data = {"nlu": []}

    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            intent = row["Intent"].lower().strip()
            example = row["Utterance"].lower().strip()
            entities = {}
            for i in range(1, 4):
                entity = row[f"Entity{i}"].lower().strip()
                value = row[f"Value{i}"].lower().strip()
                if entity and value:
                    entities[value] = entity
            example_with_entities = example
            for value, entity in entities.items():
                example_with_entities = example_with_entities.replace(value, f"[{value}]({entity})")

            found_intent = False
            for intent_data in data["nlu"]:
                if intent_data["intent"] == intent:
                    intent_data["examples"].append(example_with_entities)
                    found_intent = True
                    break

            if not found_intent:
                data["nlu"].append({"intent": intent, "examples": [example_with_entities]})

    with open(yaml_file, "w") as file:
        yaml.dump(data, file)