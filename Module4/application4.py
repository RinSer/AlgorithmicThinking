#!/usr/bin/env python
"""
This is my implementation of Application #4 from 
the Algorithmic thinking course.

created by RinSer
"""


import random
from matplotlib import pyplot as plot
import math
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
    matrix_file.close()

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


def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    """
    Takes as input two sequences seq_x and seq_y, a scoring matrix scoring_matrix, and a number of trials num_trials. 
    Returns a dictionary that represents an un-normalized distribution.
    """
    # Initialize the distribution dictionary
    scoring_distribution = dict()
    for dummy in range(num_trials):
        # Generate a random permutation of the second sequence
        list_y = list(seq_y)
        random.shuffle(list_y)
        rand_y = ''.join(list_y)
        # Compute the maximum value score for the local alignment of seq_x and seq_y using the score matrix
        current_alignment_matrix = project4.compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)
        score = project4.compute_local_alignment(seq_x, rand_y, scoring_matrix, current_alignment_matrix)[0]
        # Add the score to the distribution dictionary
        if score in scoring_distribution:
            scoring_distribution[score] += 1
        else:
            scoring_distribution[score] = 1

    return scoring_distribution


def read_words_list(file_name):
    """
    Helper function to extract the word list from a file.
    Returns the list.
    """
    words_file = open(file_name, 'r')
    words_list = list()
    for word in words_file.readlines():
        words_list.append(word.rstrip())
    words_file.close()

    return words_list


def check_spelling(checked_word, dist, word_list):
    """
    Iterates through word_list and returns the set of all words that are within edit distance dist of the string checked_word.
    """
    scoring_matrix = project4.build_scoring_matrix('abcdefghijklmnopqrstuvwxyz', 2, 1, 0)
    within_dist = set()
    for word in word_list:
        alignment_matrix = project4.compute_alignment_matrix(checked_word, word, scoring_matrix, True)
        score = project4.compute_local_alignment(checked_word, word, scoring_matrix, alignment_matrix)[0]
        edit_distance = len(checked_word)+len(word)-score
        if edit_distance <= dist:
            within_dist.add(word)

    return within_dist


# Scoring matrix dictionary
ScoringMatrix = read_scoring_matrix(SCORING_MATRIX)
# Extract the proteins' data
HumanEyeless = read_protein(HUMAN_EYELESS_PROTEIN)
FruitflyEyeless = read_protein(FRUITFLY_EYELESS_PROTEIN)


def Question1():
    """
    Function to compute the answer for Question #1.
    """
    # Compute alignment scores
    alignment_matrix = project4.compute_alignment_matrix(HumanEyeless, FruitflyEyeless, ScoringMatrix, False)
    # Compute the alignment
    eyeless_alignment = project4.compute_local_alignment(HumanEyeless, FruitflyEyeless, ScoringMatrix, alignment_matrix)

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


def Question4():
    """
    Function to draw the answer for Question #4.
    """
    scoring_distribution = generate_null_distribution(HumanEyeless, FruitflyEyeless, ScoringMatrix, 1000)
    # Generate the distribution bar plot
    scores = list()
    fractions = list()
    for score, fraction in scoring_distribution.iteritems():
        scores.append(score)
        fractions.append(fraction/1000.0)
    plot.bar(scores, fractions, color='r')
    plot.title('Null distribution of randomly generated scores.')
    plot.xlabel('Score')
    plot.ylabel('Fraction of trials total')
    plot.savefig('q4.png')
    plot.close()

    print '### Question 4 ###'
    print 'Null distribution bar plot has been saved as the file q4.png'

    return scoring_distribution


def Question5():
    """
    Function to compute the answer for Question #5.
    """
    scoring_distribution = Question4()
    # Compute the mean
    scores_sum = 0
    scores_number = 0
    for score, value in scoring_distribution.iteritems():
        for dummy in range(value):
            scores_sum += score
            scores_number += 1
    mean = scores_sum/float(scores_number)
    print scores_number
    # Compute the standard deviation
    sum_of_squared_deviations = 0
    for score, value in scoring_distribution.iteritems():
        for dummy in range(value):
            sum_of_squared_deviations += (score - mean)**2
    standard_deviation = math.sqrt(sum_of_squared_deviations/float(scores_number))
    # Compute the z-value
    z_value = (875 - mean)/standard_deviation
    # Print the results
    print '### Question 5 ###'
    print 'Mean = ' + str(mean)
    print 'Standard deviation = ' + str(standard_deviation)
    print 'Z-value = ' + str(z_value)

    return (mean, standard_deviation, z_value)


def Question8():
    """
    Function to find the answer for Question #8.
    """
    words_list = read_words_list('assets_scrabble_words3.txt')
    print '### Question 8 ###'
    print check_spelling('humble', 1, words_list)
    print check_spelling('firefly', 2, words_list)


# Execution
#Question2()
#Question5()
Question8()
