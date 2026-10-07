#!/usr/bin/env python2.7

# Basic Decision Tree program for weather-based classification
# (C) 2022-2026 Licensed under the terms of GNU GPLv3 or Later

import arff
from math import fsum, log
from numpy import add

def entropy(array):
    total = 0
    sum = fsum(array)
    for elem in array:
        if elem != 0:
            prop = elem/sum
            total += (-1) * prop * log(prop, 2)
    return total

# license doesn't cover example dataset:
file = open('weather.nominal.arff')

content = arff.load(file)

attributes = content['attributes']
data = content['data']

# Note: decision is one of the two values of last attribute

attr_num = len(attributes);
decision_idx = attr_num - 1
values_idx = 1
decisions = attributes[decision_idx][values_idx]

data_decisions = [0, 0]
data_amount = len(data)
data_entropy = 0

attr_gain_max = 0
attr_gain_max_idx = 0

for attr_reversed_idx, attribute in enumerate(reversed(attributes)):
    attr_idx = attr_num - attr_reversed_idx - 1
    attr_gain = data_entropy
    for value in attribute[values_idx]:
        value_decisions = [0, 0]
        for example in data:
            if example[attr_idx] == value:
                if example[decision_idx] == decisions[0]:
                    value_decisions[0] += 1
                elif example[decision_idx] == decisions[1]:
                    value_decisions[1] += 1
        value_entropy = entropy(value_decisions)
        if attr_idx == decision_idx:
            data_decisions = add(data_decisions, value_decisions)
        else:
            attr_gain -= value_entropy * fsum(value_decisions) / data_amount
            print value, attr_gain
    if attr_idx == decision_idx:
        data_entropy = entropy(data_decisions)
    else:
        if attr_gain > attr_gain_max:
            attr_gain_max = attr_gain
            attr_gain_max_idx = attr_idx
        print attribute, attr_gain

print attributes[attr_gain_max_idx]
