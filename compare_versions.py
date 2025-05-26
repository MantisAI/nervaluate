from nervaluate.evaluator import Evaluator as NewEvaluator
from nervaluate import Evaluator as OldEvaluator
from nervaluate.reporting import summary_report_overall_indices, summary_report_ents_indices, summary_report

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


def overall_report(true, pred):

    new_evaluator = NewEvaluator(true, pred, tags=['PER', 'ORG', 'LOC', 'DATE'], loader="list")
    print(new_evaluator.summary_report())

    print("-"*100)

    old_evaluator = OldEvaluator(true, pred, tags=['PER', 'ORG', 'LOC', 'DATE'], loader="list")
    results = old_evaluator.evaluate()[0]  # Get the first element which contains the overall results
    print(summary_report(results))


def entities_report(true, pred):

    new_evaluator = NewEvaluator(true, pred, tags=['PER', 'ORG', 'LOC', 'DATE'], loader="list")

    # entities - strict, exact, partial, ent_type
    print(new_evaluator.summary_report(mode="entities", scenario="strict"))
    print(new_evaluator.summary_report(mode="entities", scenario="exact"))
    print(new_evaluator.summary_report(mode="entities", scenario="partial"))
    print(new_evaluator.summary_report(mode="entities", scenario="ent_type"))

    print("-"*100)

    old_evaluator = OldEvaluator(true, pred, tags=['PER', 'ORG', 'LOC', 'DATE'], loader="list")
    _, results_agg_entities_type, _, _ = old_evaluator.evaluate()  # Get the second element which contains the entity-specific results
    print(summary_report(results_agg_entities_type, mode="entities", scenario="strict"))
    print(summary_report(results_agg_entities_type, mode="entities", scenario="exact"))
    print(summary_report(results_agg_entities_type, mode="entities", scenario="partial"))
    print(summary_report(results_agg_entities_type, mode="entities", scenario="ent_type"))


def indices_report_overall(true, pred):
    
    true = [
        [{"label": "PER", "start": 2, "end": 4}],
        [{"label": "LOC", "start": 1, "end": 2}, {"label": "LOC", "start": 3, "end": 4}]]
    
    pred = [
        [{"label": "PER", "start": 2, "end": 4}],
        [{"label": "LOC", "start": 1, "end": 2},
         {"label": "LOC", "start": 3, "end": 4}]
    ]

    new_evaluator = NewEvaluator(true, pred, tags=['PER', 'LOC', 'DATE'], loader="list")
    print(new_evaluator.summary_report_indices(colors=True, mode="overall", scenario="strict"))
    print(new_evaluator.summary_report_indices(colors=True, mode="overall", scenario="exact"))
    print(new_evaluator.summary_report_indices(colors=True, mode="overall", scenario="partial"))
    print(new_evaluator.summary_report_indices(colors=True, mode="overall", scenario="ent_type"))

    old_evaluator = OldEvaluator(true, pred, tags=['LOC', 'PER'])
    results, results_per_tag, result_indices, result_indices_by_tag = old_evaluator.evaluate()
    print(summary_report_overall_indices(evaluation_indices=result_indices, error_schema='strict', preds=pred))
    print(summary_report_overall_indices(evaluation_indices=result_indices, error_schema='exact', preds=pred))
    print(summary_report_overall_indices(evaluation_indices=result_indices, error_schema='partial', preds=pred))
    print(summary_report_overall_indices(evaluation_indices=result_indices, error_schema='ent_type', preds=pred))
    

if __name__ == "__main__":
    tags = ['PER', 'ORG', 'LOC', 'DATE']
    true, pred = generate_synthetic_data(tags, num_samples=10)

    # overall_report(true, pred)
    # print("\n\n" + "="*100 + "\n\n")
    # entities_report(true, pred)
    # print("\n\n" + "="*100 + "\n\n")
    indices_report_overall(true, pred)
