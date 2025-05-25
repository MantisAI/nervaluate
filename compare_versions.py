from nervaluate.evaluator import Evaluator as NewEvaluator
from nervaluate import Evaluator as OldEvaluator

from nervaluate.reporting import summary_report_overall_indices, summary_report_ents_indices, summary_report_overall

def overall_report():

    true = [
        # "The John Smith who works at Google Inc"
        ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-ORG', 'I-ORG'],

    ]

    pred = [
    # "The John Smith who works at Google Inc"
    
    # Strict:   exact boundary surface string match and entity type
    #
    ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-ORG', 'I-ORG'],     # strict - correct: 2 incorrect: 0 partial: 0 missed: 0 spurious: 0
    # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'O', 'O'],             # strict - correct: 1 incorrect: 0 partial: 0 missed: 1 spurious: 0
    # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-LOC', 'I-LOC'],     # strict - correct: 1 incorrect: 1 partial: 0 missed: 0 spurious: 0 
    # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-LOC', 'O'],         # strict - correct: 1 incorrect: 1 partial: 0 missed: 0 spurious: 0
    # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'O', 'B-LOC'],         # strict - correct: 1 incorrect: 1 partial: 0 missed: 0 spurious: 0
    # ['O', 'B-PER', 'I-PER', 'O', 'B-PER', 'O', 'B-LOC', 'I-LOC'], # strict - correct: 1 incorrect: 1 partial: 0 missed: 0 spurious: 1


    # Type:     must have the same tag and some minimum overlap between the system tagged entity and the gold annotation
    #
    # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-ORG', 'I-ORG'],     # ent_type - correct: 2 incorrect: 0 partial: 0 missed: 0 spurious: 0
    # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'O', 'O'],             # ent_type - correct: 1 incorrect: 0 partial: 0 missed: 1 spurious: 0
    # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-LOC', 'I-LOC'],     # ent_type - correct: 1 incorrect: 1 partial: 0 missed: 0 spurious: 0
    # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-LOC', 'O'],         # ent_type - correct: 1 incorrect: 1 partial: 0 missed: 0 spurious: 0   -> Needs fixing! (old code)
    # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'O', 'B-LOC'],         # ent_type - correct: 1 incorrect: 1 partial: 0 missed: 0 spurious: 0
    # ['O', 'B-PER', 'I-PER', 'O', 'B-PER', 'O', 'B-LOC', 'I-LOC'], # ent_type - correct: 1 incorrect: 1 partial: 0 missed: 0 spurious: 1
    
    # Exact: exact boundary match over the surface string, regardless of the type
    #
    # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-ORG', 'I-ORG'],     # exact - correct: 2 incorrect: 0 partial: 0 missed: 0 spurious: 0
    # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'O', 'O'],             # exact - correct: 1 incorrect: 0 partial: 0 missed: 1 spurious: 0
    # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-LOC', 'I-LOC'],     # exact - correct: 2 incorrect: 0 partial: 0 missed: 0 spurious: 0
    # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-LOC', 'O'],         # exact - correct: 1 incorrect: 1 partial: 0 missed: 0 spurious: 0
    # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'O', 'B-LOC'],         # exact - correct: 1 incorrect: 1 partial: 0 missed: 0 spurious: 0
    # ['O', 'B-PER', 'I-PER', 'O', 'B-PER', 'O', 'B-LOC', 'I-LOC'], # exact - correct: 2 incorrect: 0 partial: 0 missed: 0 spurious: 1


    # Partial: partial boundary match over the surface string, regardless of the type
    #
    # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-ORG', 'I-ORG'],     # partial - correct: 2 incorrect: 0 partial: 0 missed: 0 spurious: 0
    # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'O', 'O'],             # partial - correct: 1 incorrect: 0 partial: 0 missed: 1 spurious: 0
    # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-LOC', 'I-LOC'],     # partial - correct: 2 incorrect: 0 partial: 0 missed: 0 spurious: 0        
    # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-LOC', 'O'],         # partial - correct: 1 incorrect: 0 partial: 1 missed: 0 spurious: 0 
    # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'O', 'B-LOC'],         # partial - correct: 1 incorrect: 0 partial: 1 missed: 0 spurious: 0
    # ['O', 'B-PER', 'I-PER', 'O', 'B-PER', 'O', 'B-LOC', 'I-LOC'], # partial - correct: 2 incorrect: 0 partial: 0 missed: 0 spurious: 1
]

    new_evaluator = NewEvaluator(true, pred, tags=['PER', 'ORG', 'LOC', 'DATE'], loader="list")
    print(new_evaluator.summary_report())

    old_evaluator = OldEvaluator(true, pred, tags=['PER', 'ORG', 'LOC', 'DATE'], loader="list")
    results = old_evaluator.evaluate()[0]  # Get the first element which contains the overall results
    print(summary_report_overall(results))

def entities_report():

    # "In Paris Marie Curie lived in 1895"
    # true = [['O', 'B-LOC', 'B-PER', 'I-PER', 'O', 'O', 'B-DATE']]
    # pred = [['O', 'B-LOC', 'I-LOC', 'O', 'B-PER', 'O', 'B-DATE']]

    # "The John Smith who works at Google Inc"
    true = [['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-ORG', 'I-ORG']]
    pred = [
            # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-ORG', 'I-ORG']
            # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'O', 'O'],  
            # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-LOC', 'I-LOC'],
            # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-LOC', 'O'],
            # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'O', 'B-LOC'],
            ['O', 'B-PER', 'B-LOC', 'O', 'B-PER', 'O', 'B-ORG', 'I-LOC'],
        ]
    

    new_evaluator = NewEvaluator(true, pred, tags=['PER', 'ORG', 'LOC', 'DATE'], loader="list")

    # entities - strict, exact, partial, ent_type
    print(new_evaluator.summary_report(mode="entities", scenario="strict"))
    print(new_evaluator.summary_report(mode="entities", scenario="exact"))
    print(new_evaluator.summary_report(mode="entities", scenario="partial"))
    print(new_evaluator.summary_report(mode="entities", scenario="ent_type"))


def indices_report():

    # "The John Smith who works at Google Inc"

    """    
    ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-LOC', 'I-LOC'],
    ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-LOC', 'O'],
    ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'O', 'B-LOC'],
    ['O', 'B-PER', 'B-LOC', 'O', 'B-PER', 'O', 'B-ORG', 'I-LOC']
    """

    true = [
        ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-ORG', 'I-ORG'],
        ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-ORG', 'I-ORG'],
        ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-ORG', 'I-ORG']
        ]
    pred = [
        ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-ORG', 'I-ORG'],
        ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'O', 'B-LOC'],
        ['O', 'B-PER', 'B-LOC', 'O', 'B-PER', 'O', 'B-ORG', 'I-LOC']
        ]
    
    new_evaluator = NewEvaluator(true, pred, tags=['PER', 'ORG', 'LOC', 'DATE'], loader="list")
    print(new_evaluator.summary_report_indices(colors=True))

def generate_synthetic_data(tags, num_samples, min_length=5, max_length=15):
    """
    Generate synthetic NER data with ground truth and predictions.
    
    Args:
        tags (list): List of entity tags to use (e.g., ['PER', 'ORG', 'LOC', 'DATE'])
        num_samples (int): Number of samples to generate
        min_length (int): Minimum sequence length
        max_length (int): Maximum sequence length
    
    Returns:
        tuple: (true_sequences, pred_sequences)
    """
    import random
    
    def generate_sequence(length):
        sequence = ['O'] * length
        # Randomly decide if we'll add an entity
        if random.random() < 0.7:  # 70% chance to add an entity
            # Choose random tag
            tag = random.choice(tags)
            # Choose random start position
            start = random.randint(0, length - 2)
            # Choose random length (1 or 2 tokens)
            entity_length = random.randint(1, 2)
            if start + entity_length <= length:
                sequence[start] = f'B-{tag}'
                for i in range(1, entity_length):
                    sequence[start + i] = f'I-{tag}'
        return sequence
    
    def generate_prediction(true_sequence):
        pred_sequence = true_sequence.copy()
        # Randomly modify some predictions
        for i in range(len(pred_sequence)):
            if random.random() < 0.2:  # 20% chance to modify each token
                if pred_sequence[i] == 'O':
                    # Sometimes predict an entity where there isn't one
                    if random.random() < 0.3:
                        tag = random.choice(tags)
                        pred_sequence[i] = f'B-{tag}'
                else:
                    # Sometimes change the entity type or boundary
                    if random.random() < 0.3:
                        tag = random.choice(tags)
                        if pred_sequence[i].startswith('B-'):
                            pred_sequence[i] = f'B-{tag}'
                        elif pred_sequence[i].startswith('I-'):
                            pred_sequence[i] = f'I-{tag}'
                    elif random.random() < 0.3:
                        # Sometimes predict O instead of an entity
                        pred_sequence[i] = 'O'
        return pred_sequence
    
    true_sequences = []
    pred_sequences = []
    
    for _ in range(num_samples):
        length = random.randint(min_length, max_length)
        true_sequence = generate_sequence(length)
        pred_sequence = generate_prediction(true_sequence)
        true_sequences.append(true_sequence)
        pred_sequences.append(pred_sequence)
    
    return true_sequences, pred_sequences

if __name__ == "__main__":
    #overall_report()
    #entities_report()
    #indices_report()
    
    # Example usage of generate_synthetic_data
    tags = ['PER', 'ORG', 'LOC', 'DATE']
    true, pred = generate_synthetic_data(tags, num_samples=30)
    print("Generated synthetic data:")
    print("Ground truth:", true)
    print("Predictions:", pred)