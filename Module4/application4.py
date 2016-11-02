#!/usr/bin/env python
"""
This is my implementation of Application #4 from 
the Algorithmic thinking course.

created by RinSer
"""


import project4


# File names
HUMAN_EYELESS_PROTEIN = 'HumanEyelessProtein.txt'
FRUITFLY_EYELESS_PROTEIN = 'FruitflyEyelessProtein.txt'
CONSENSUS_PAX_DOMAIN = 'ConsensusPAXDomain.txt'
SCORING_MATRIX = 'PAM50.txt'


def read_protein(file_name):
    """
    Helper function to read protein sequence from a file.
    Returns the sequence as a string.
    """
    protein_file = open(file_name, 'r')
    protein_sequence = protein_file.read().rstrip()
    protein_file.close()
    
    return protein_sequence


def read_scoring_matrix(file_name):
    """
    Helper function to read a scoring matrix from a file.
    Returns the scoring matrix as a dictionary.
    """
    matrix_file = open(file_name, 'r')
    scoring_matrix = dict()
    # Read the first line and create a list
    column_values = matrix_file.readline().split()
    # Read the other lines
    for line in matrix_file.readlines():
        scores = line.split()
        row_value = scores.pop(0)
        scoring_matrix[row_value] = dict()
        for column_value, score in zip(column_values, scores):
            scoring_matrix[row_value][column_value] = int(score)

    return scoring_matrix


def remove_dashes(string):
    """
    Helper function to remove dashes from a given string.
    Returns the string without dashes.
    """
    dashless = ''
    for character in string:
        if character != '-':
            dashless += character

    return dashless 


def compare_strings(string1, string2):
    """
    Helper function to compare the characters in two strings of equal size.
    Returns the percentage number of equal characters as a floating point number.
    """
    number_of_equals = 0
    if len(string1) == len(string2):
        for idx_c in range(len(string1)):
            if string1[idx_c] == string2[idx_c]:
                number_of_equals += 1
    
    return number_of_equals/float(len(string1))*100


# Scoring matrix dictionary
ScoringMatrix = read_scoring_matrix(SCORING_MATRIX)


def Question1():
    """
    Function to compute the answer for Question #1.
    """
    # Extract the data
    human_eyeless = read_protein(HUMAN_EYELESS_PROTEIN)
    fruitfly_eyeless = read_protein(FRUITFLY_EYELESS_PROTEIN)
    # Compute alignment scores
    alignment_matrix = project4.compute_alignment_matrix(human_eyeless, fruitfly_eyeless, ScoringMatrix, False)
    # Compute the alignment
    eyeless_alignment = project4.compute_local_alignment(human_eyeless, fruitfly_eyeless, ScoringMatrix, alignment_matrix)

    print '### Question 1 ###'
    print 'Score: ' + str(eyeless_alignment[0])
    print eyeless_alignment[1]
    print eyeless_alignment[2]
    
    return eyeless_alignment


def Question2():
    """
    Function to compute the answer for Question #2.
    """
    # Extract the consensus data
    consensus_pax = read_protein(CONSENSUS_PAX_DOMAIN)
    # Find the local alignments from Question 1
    local_alignments = Question1()
    human_pax = remove_dashes(local_alignments[1])
    fruitfly_pax = remove_dashes(local_alignments[2])
    # Compute the global alignments
    # For human
    humcon_alignment = project4.compute_alignment_matrix(human_pax, consensus_pax, ScoringMatrix, True)
    human_global = project4.compute_global_alignment(human_pax, consensus_pax, ScoringMatrix, humcon_alignment)
    human_percentage = compare_strings(human_global[1], human_global[2])
    # For fruitfly
    flycon_alignment = project4.compute_alignment_matrix(fruitfly_pax, consensus_pax, ScoringMatrix, True)
    fruitfly_global = project4.compute_global_alignment(fruitfly_pax, consensus_pax, ScoringMatrix, flycon_alignment)
    fruitfly_percentage = compare_strings(fruitfly_global[1], fruitfly_global[2])

    print '### Question 2 ###'
    print 'Human percentage of agreed elements: ' + str(human_percentage) + '%'
    print 'Fruit fly percentage of agreed elements: ' + str(fruitfly_percentage) + '%'


# Execution
Question2()
