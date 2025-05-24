from nervaluate.evaluator import Evaluator

def overall_report():

    true = [
        # "The John Smith who works at Google Inc"
        ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-ORG', 'I-ORG'],

    ]

    pred = [
    # "The John Smith who works at Google Inc"
    
    # Strict:   exact boundary surface string match and entity type
    #
    # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-ORG', 'I-ORG'],     # strict - correct: 2 incorrect: 0 partial: 0 missed: 0 spurious: 0
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

    new_evaluator = Evaluator(true, pred, tags=['PER', 'ORG', 'LOC', 'DATE'], loader="list")
    print(new_evaluator.summary_report())

    from nervaluate import Evaluator
    old_evaluator = Evaluator(true, pred, tags=['PER', 'ORG', 'LOC', 'DATE'], loader="list")

    from nervaluate.reporting import summary_report_overall_indices, summary_report_ents_indices, summary_report_overall
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
        ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'O', 'O'],             # strict - correct: 1 incorrect: 0 partial: 0 missed: 1 spurious: 0
        ]
    

    new_evaluator = Evaluator(true, pred, tags=['PER', 'ORG', 'LOC', 'DATE'], loader="list")

    # entities - strict, exact, partial, ent_type
    print(new_evaluator.summary_report(mode="entities", scenario="strict"))
    print(new_evaluator.summary_report(mode="entities", scenario="exact"))
    print(new_evaluator.summary_report(mode="entities", scenario="partial"))
    print(new_evaluator.summary_report(mode="entities", scenario="ent_type"))


def indices_report(results):
    # indices
    # print(new_evaluator.summary_report_indices())   # TODO: make this output better
    pass


if __name__ == "__main__":
    # overall_report()
    entities_report()