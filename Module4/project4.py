"""
My implementation of the Algorithmic thinking 
project #4.

created by RinSer
"""


def string_to_set(string):
    """
    Helper function to convert a string into a set of characters 
    contained in a given string.
    Takes a string as input.
    Returns a set of characters.
    """
    alphabet = set([])
    for character in string:
        alphabet.add(character)

    return alphabet


def print_scoring_matrix(matrix, alphabet_string):
    """
    Helper function to print a scoring matrix.
    Returns nothing.
    """
    header = ' '
    for character in alphabet_string+'-':
        header += '  '+character
    print header
    for character_i in alphabet_string+'-':
        character_row = character_i
        for character_j in alphabet_string+'-':
            score = str(matrix[character_i][character_j])
            if len(score) < 2:
                score = ' '+score
            character_row += ' '+score
        print character_row


def print_alignment_matrix(matrix, seq_x, seq_y):
    """
    Helper function to print an alignment matrix.
    Returns nothing.
    """
    header = ' '
    for character in '-'+seq_y:
        header += '  '+character
    print header
    for idx_i in range(len('-'+seq_x)):
        character_row = ('-'+seq_x)[idx_i]
        for idx_j in range(len('-'+seq_y)):
            score = str(matrix[idx_i][idx_j])
            if len(score) < 2:
                score = ' '+score
            character_row += ' '+score
        print character_row


def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Takes as input a set of characters alphabet and three scores diag_score, off_diag_score, and dash_score. The function returns a dictionary of dictionaries whose entries are indexed by pairs of characters in alphabet plus '-'. The score for any entry indexed by one or more dashes is dash_score. The score for the remaining diagonal entries is diag_score. Finally, the score for the remaining off-diagonal entries is off_diag_score.
    """
    # Add a dash to the alphabet
    alphabet = set(alphabet)
    alphabet.add('-')
    # Initialize the matrix
    scoring_matrix = dict()
    # Populate the matrix
    for character_i in alphabet:
        scoring_matrix[character_i] = dict()
        for character_j in alphabet:
            if character_i == '-' or character_j == '-':
                scoring_matrix[character_i][character_j] = dash_score
            elif character_i != character_j:
                scoring_matrix[character_i][character_j] = off_diag_score
            else:
                scoring_matrix[character_i][character_j] = diag_score

    return scoring_matrix


def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    Takes as input two sequences seq_x and seq_y whose elements share a common alphabet with the scoring matrix scoring_matrix. The function computes and returns the alignment matrix for seq_x and seq_y as described in the Homework. If global_flag is True, each entry of the alignment matrix is computed using the method described in Question 8 of the Homework. If global_flag is False, each entry is computed using the method described in Question 12 of the Homework.
    """
    # Initialize the alignment matrix
    alignment_matrix = [[] for dummy in range(len(seq_x)+1)]
    alignment_matrix[0].append(0)
    # First column    
    for idx_i in range(1, len(seq_x)+1):
        score = alignment_matrix[idx_i-1][0] + scoring_matrix[seq_x[idx_i-1]]['-']
        if not global_flag and score < 0:
            score = 0
        alignment_matrix[idx_i].append(score)
    # First row
    for idx_j in range(1, len(seq_y)+1):
        score = alignment_matrix[0][idx_j-1] + scoring_matrix['-'][seq_y[idx_j-1]]
        if not global_flag and score < 0:
            score = 0
        alignment_matrix[0].append(score)
    # Main scores
    for idx_i in range(1, len(seq_x)+1):
        for idx_j in range(1, len(seq_y)+1):
            no_dash = alignment_matrix[idx_i-1][idx_j-1] + scoring_matrix[seq_x[idx_i-1]][seq_y[idx_j-1]]
            x_dash = alignment_matrix[idx_i-1][idx_j] + scoring_matrix[seq_x[idx_i-1]]['-']
            y_dash = alignment_matrix[idx_i][idx_j-1] + scoring_matrix['-'][seq_y[idx_j-1]]
            score = max(no_dash, x_dash, y_dash)
            if not global_flag and score < 0:
                score = 0
            alignment_matrix[idx_i].append(score)

    return alignment_matrix


def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Takes as input two sequences seq_x and seq_y whose elements share a common alphabet with the scoring matrix scoring_matrix. This function computes a global alignment of seq_x and seq_y using the global alignment matrix alignment_matrix.The function returns a tuple of the form (score, align_x, align_y) where score is the score of the global alignment align_x and align_y. Note that align_x and align_y should have the same length and may include the padding character '-'.
    """
    # Initialize the indices and aligned sequences
    idx_i = len(seq_x)
    idx_j = len(seq_y)
    aligned_x = ''
    aligned_y = ''
    score = alignment_matrix[idx_i][idx_j]
    # Find the aligned sequences
    while idx_i > 0 and idx_j > 0:
        if alignment_matrix[idx_i][idx_j] == alignment_matrix[idx_i-1][idx_j-1] + scoring_matrix[seq_x[idx_i-1]][seq_y[idx_j-1]]:
            aligned_x = seq_x[idx_i-1] + aligned_x
            aligned_y = seq_y[idx_j-1] + aligned_y
            idx_i -= 1
            idx_j -= 1
        elif alignment_matrix[idx_i][idx_j] == alignment_matrix[idx_i-1][idx_j] + scoring_matrix[seq_x[idx_i-1]]['-']:
            aligned_x = seq_x[idx_i-1] + aligned_x
            aligned_y = '-' + aligned_y
            idx_i -= 1
        elif alignment_matrix[idx_i][idx_j] == alignment_matrix[idx_i][idx_j-1] + scoring_matrix['-'][seq_y[idx_j-1]]:
            aligned_x = '-' + aligned_x
            aligned_y = seq_y[idx_j-1] + aligned_y
            idx_j -= 1
    # Add residual symbols and ending dashes if necessary
    while idx_i > 0:
        aligned_x = seq_x[idx_i-1] + aligned_x
        aligned_y = '-' + aligned_y
        idx_i -= 1
    while idx_j > 0:
        aligned_x = '-' + aligned_x
        aligned_y = seq_y[idx_j-1] + aligned_y
        idx_j -= 1

    return (score, aligned_x, aligned_y)


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Takes as input two sequences seq_x and seq_y whose elements share a common alphabet with the scoring matrix scoring_matrix. This function computes a local alignment of seq_x and seq_y using the local alignment matrix alignment_matrix.The function returns a tuple of the form (score, align_x, align_y) where score is the score of the optimal local alignment align_x and align_y. Note that align_x and align_y should have the same length and may include the padding character '-'.
    """
    # Find the maximum score
    max_i = None
    max_j = None
    max_score = 0
    for idx_i in range(len(alignment_matrix)):
        for idx_j in range(len(alignment_matrix[idx_i])):
            if alignment_matrix[idx_i][idx_j] > max_score:
                max_score = alignment_matrix[idx_i][idx_j]
                max_i = idx_i
                max_j = idx_j
    score = max_score
    # Find the aligned sequences
    aligned_x = ''
    aligned_y = ''
    while max_score > 0:
        if alignment_matrix[max_i][max_j] == alignment_matrix[max_i-1][max_j-1] + scoring_matrix[seq_x[max_i-1]][seq_y[max_j-1]]:
            aligned_x = seq_x[max_i-1] + aligned_x
            aligned_y = seq_y[max_j-1] + aligned_y
            max_score = alignment_matrix[max_i-1][max_j-1]
            max_i -= 1
            max_j -= 1
        elif alignment_matrix[max_i][max_j] == alignment_matrix[max_i-1][max_j] + scoring_matrix[seq_x[max_i-1]]['-']:
            aligned_x = seq_x[max_i-1] + aligned_x
            aligned_y = '-' + aligned_y
            max_score = alignment_matrix[max_i-1][max_j]
            max_i -= 1
        elif alignment_matrix[max_i][max_j] == alignment_matrix[max_i][max_j-1] + scoring_matrix['-'][seq_y[max_j-1]]:
            aligned_x = '-' + aligned_x
            aligned_y = seq_y[max_j-1] + aligned_y
            max_score = alignment_matrix[max_i][max_j-1]
            max_j -= 1

    return (score, aligned_x, aligned_y)


# Testing
#DNA_string = 'ACTG'
#latin_string = 'abcdefghijklmnopqrstuvwxyz'
# Create scoring matrices
#DNA_matrix = build_scoring_matrix(string_to_set(DNA_string), 10, 4, -6)
#latin_matrix = build_scoring_matrix(string_to_set(latin_string), 10, 2, -5)
#print_scoring_matrix(DNA_matrix, DNA_string)
#print_scoring_matrix(latin_matrix, latin_string)
#DNA_alignment = compute_alignment_matrix('AA', 'TAAT', DNA_matrix, False)
#print_alignment_matrix(DNA_alignment, 'AA', 'TAAT')
#print compute_local_alignment('AA', 'TAAT', DNA_matrix, DNA_alignment)
