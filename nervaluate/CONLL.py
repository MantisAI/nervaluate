#!/usr/bin/env python3
# coding: utf-8



example = ",\tO\nDavos\tPERSON\n2018\tO\n:\tO\nSoros\tPERSON\naccuses\tO\nTrump\tPERSON\nof\tO\nwanting\tO\na\tO\n`\tO\nmafia\tO\nstate\tO\n'\tO\nand\tO\nblasts\tO\nsocial\tO\nmedia\tO\n.\tO\n"

def CONLL_to_spans(doc):

    # TODO: handle multi-token entities
    # this simple example only handles single tokens

    doc = doc.split("\n")

    if doc[-1] == "":
        doc = doc[:-1]

    out = [list_to_prodigy(token, i) for i, token in enumerate(doc)]

    return out


def list_to_prodigy(tokens_str, i):

    tokens = tokens_str.split("\t")

    return {"label": tokens[1], "start": i, "end": i}


[print(i) for i in CONLL_to_spans(example)]
