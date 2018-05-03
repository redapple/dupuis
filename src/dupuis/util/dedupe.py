#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from builtins import input

import sys

from dedupe.convenience import unique
from veryprettytable import VeryPrettyTable


def consoleLabel(deduper, additional_columns=[]): # pragma: no cover
    '''
    Command line interface for presenting and labeling training pairs
    by the user

    Argument :
    A deduper object
    '''

    finished = False
    use_previous = False
    fields = unique(field.field
                    for field
                    in deduper.data_model.primary_fields)

    buffer_len = 1 # Max number of previous operations
    examples_buffer = []
    uncertain_pairs = []

    while not finished :
        if use_previous:
            record_pair, _ = examples_buffer.pop(0)
            use_previous = False
        else:
            if not uncertain_pairs:
                uncertain_pairs = deduper.uncertainPairs()
            record_pair = uncertain_pairs.pop()

        n_match = (len(deduper.training_pairs['match']) +
                   sum(label=='match' for _, label in examples_buffer))
        n_distinct = (len(deduper.training_pairs['distinct']) +
                      sum(label=='distinct' for _, label in examples_buffer))

        x = VeryPrettyTable()
        columns = fields + additional_columns
        x.field_names = columns
        x.align = "l"
        for pair in record_pair:
            x.add_row(list(pair[field] for field in columns))
        print(x)
        print("{0}/10 positive, {1}/10 negative".format(n_match, n_distinct),
                file=sys.stderr)
        print('Do these records refer to the same thing?', file=sys.stderr)

        valid_response = False
        user_input = ''
        while not valid_response:
            if examples_buffer:
                prompt = '(y)es / (n)o / (u)nsure / (f)inished / (p)revious'
                valid_responses = {'y', 'n', 'u', 'f', 'p'}
            else:
                prompt = '(y)es / (n)o / (u)nsure / (f)inished'
                valid_responses = {'y', 'n', 'u', 'f'}

            print(prompt, file=sys.stderr)
            user_input = input()
            if user_input in valid_responses:
                valid_response = True

        if user_input == 'y':
            examples_buffer.insert(0, (record_pair, 'match'))
        elif user_input == 'n' :
            examples_buffer.insert(0, (record_pair, 'distinct'))
        elif user_input == 'u':
            examples_buffer.insert(0, (record_pair, 'uncertain'))
        elif user_input == 'f':
            print('Finished labeling', file=sys.stderr)
            finished = True
        elif user_input == 'p':
            use_previous = True
            uncertain_pairs.append(record_pair)

        if len(examples_buffer) > buffer_len:
            record_pair, label = examples_buffer.pop()
            if label in ['distinct', 'match']:
                examples = {'distinct' : [], 'match' : []}
                examples[label].append(record_pair)
                deduper.markPairs(examples)

    for record_pair, label in examples_buffer:
        if label in ['distinct', 'match']:
            examples = {'distinct' : [], 'match' : []}
            examples[label].append(record_pair)
            deduper.markPairs(examples)
