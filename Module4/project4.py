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
    alignment_matrix = [[] for idx_x in range(len(seq_x)+1)]
    alignment_matrix[0].append(0)
    # First column    
    for idx_i in range(1, len(seq_x)+1):
        alignment_matrix[idx_i].append(alignment_matrix[idx_i-1][0] + scoring_matrix[seq_x[idx_i-1]]['-'])
    # First row
    for idx_j in range(1, len(seq_y)+1):
        alignment_matrix[0].append(alignment_matrix[0][idx_j-1] + scoring_matrix['-'][seq_y[idx_j-1]])
    # Main scores
    for idx_i in range(1, len(seq_x)+1):
        for idex_j in range(1, len(seq_y)+1):
            no_dash = alignment_matrix[idx_i-1][idx_j-1] + scoring_matrix[seq_x[idx_i-1]][seq_y[idx_j-1]]
            x_dash = alignment_matrix[idx_i-1][idx_j-1] + scoring_matrix[seq_x[idx_i-1]]['-']
            y_dash = alignment_matrix[idx_i-1][idx_j] + scoring_matrix['-'][seq_y[idx_j-1]]
            alignment_matrix[idx_i].append(max(no_dash, x_dash, y_dash))

    return alignment_matrix


# Testing
DNA_string = 'ACTG'
latin_string = 'abcdefghijklmnopqrstuvwxyz'
# Create scoring matrices
DNA_matrix = build_scoring_matrix(string_to_set(DNA_string), 5, 2, -2)
latin_matrix = build_scoring_matrix(string_to_set(latin_string), 10, 2, -5)
#print_scoring_matrix(DNA_matrix, DNA_string)
#print_scoring_matrix(latin_matrix, latin_string)
DNA_alignment = compute_alignment_matrix('AC', 'TAA', DNA_matrix, False)
print_alignment_matrix(DNA_alignment, 'AC', 'TAA')
