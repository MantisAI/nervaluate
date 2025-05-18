import nltk
import sklearn_crfsuite
from sklearn.metrics import classification_report

from nervaluate import Evaluator, collect_named_entities, summary_report_ent, summary_report_overall


def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]

    features = {
        "bias": 1.0,
        "word.lower()": word.lower(),
        "word[-3:]": word[-3:],
        "word[-2:]": word[-2:],
        "word.isupper()": word.isupper(),
        "word.istitle()": word.istitle(),
        "word.isdigit()": word.isdigit(),
        "postag": postag,
        "postag[:2]": postag[:2],
    }
    if i > 0:
        word1 = sent[i - 1][0]
        postag1 = sent[i - 1][1]
        features.update(
            {
                "-1:word.lower()": word1.lower(),
                "-1:word.istitle()": word1.istitle(),
                "-1:word.isupper()": word1.isupper(),
                "-1:postag": postag1,
                "-1:postag[:2]": postag1[:2],
            }
        )
    else:
        features["BOS"] = True

    if i < len(sent) - 1:
        word1 = sent[i + 1][0]
        postag1 = sent[i + 1][1]
        features.update(
            {
                "+1:word.lower()": word1.lower(),
                "+1:word.istitle()": word1.istitle(),
                "+1:word.isupper()": word1.isupper(),
                "+1:postag": postag1,
                "+1:postag[:2]": postag1[:2],
            }
        )
    else:
        features["EOS"] = True

    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    return [label for token, postag, label in sent]


def sent2tokens(sent):
    return [token for token, postag, label in sent]


def main():
    print("Loading CoNLL 2002 NER Spanish data")
    nltk.corpus.conll2002.fileids()
    train_sents = list(nltk.corpus.conll2002.iob_sents("esp.train"))
    test_sents = list(nltk.corpus.conll2002.iob_sents("esp.testb"))

    x_train = [sent2features(s) for s in train_sents]
    y_train = [sent2labels(s) for s in train_sents]

    x_test = [sent2features(s) for s in test_sents]
    y_test = [sent2labels(s) for s in test_sents]

    print("Train a CRF on the CoNLL 2002 NER Spanish data")
    crf = sklearn_crfsuite.CRF(algorithm="lbfgs", c1=0.1, c2=0.1, max_iterations=10, all_possible_transitions=True)
    try:
        crf.fit(x_train, y_train)
    except AttributeError:
        pass

    y_pred = crf.predict(x_test)
    labels = list(crf.classes_)
    labels.remove("O")  # remove 'O' label from evaluation
    sorted_labels = sorted(labels, key=lambda name: (name[1:], name[0]))  # group B- and I- results
    y_test_flat = [y for msg in y_test for y in msg]
    y_pred_flat = [y for msg in y_pred for y in msg]
    print(classification_report(y_test_flat, y_pred_flat, labels=sorted_labels))

    test_sents_labels = []
    for sentence in test_sents:
        sentence = [token[2] for token in sentence]
        test_sents_labels.append(sentence)

    pred_collected = [collect_named_entities(msg) for msg in y_pred]
    test_collected = [collect_named_entities(msg) for msg in y_test]

    evaluator = Evaluator(test_collected, pred_collected, ["LOC", "MISC", "PER", "ORG"])
    results, results_agg = evaluator.evaluate()

    print("\n\nOverall")
    print(summary_report_overall(results))
    print("\n\n'Strict'")
    print(summary_report_ent(results_agg, scenario="strict"))
    print("\n\n'Ent_Type'")
    print(summary_report_ent(results_agg, scenario="ent_type"))
    print("\n\n'Partial'")
    print(summary_report_ent(results_agg, scenario="partial"))
    print("\n\n'Exact'")
    print(summary_report_ent(results_agg, scenario="exact"))


if __name__ == "__main__":
    main()
