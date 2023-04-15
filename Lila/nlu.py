# import rasa_nlu
# from rasa_nlu.training_data import load_data
# from rasa_nlu.model import Trainer
# from rasa_nlu import config
# from rasa_nlu.model import Metadata, Interpreter
#
#
# # Load the training data
# training_data = load_data('test_conversion.yaml')
#
# # Set the configuration for the NLU pipeline
# pipeline_configuration = config.load("config_spacy.yml")
#
# # Create a trainer that uses the pipeline configuration
# trainer = Trainer(pipeline_configuration)
#
# # Train the model on the data and save to disk for later use
# model_directory = trainer.persist('models/nlu', fixed_model_name='test_conversion', training_data=training_data)
#
# # Load the saved model from disk
# interpreter = Interpreter.load(model_directory)
#
# # Test the model on some sample input
# result = interpreter.parse("I want to order a pizza with pepperoni and mushrooms")
# print(result)