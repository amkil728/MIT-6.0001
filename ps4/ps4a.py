# Problem Set 4A
# Name: amkil728


def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    # If sequence is of length 1, i.e., a single character
    if len(sequence) == 1:
        # The only permutation is the string itself
        return [sequence]

    # Otherwise, sequence has multiple permutations

    permutations = list() # list to store permutations of sequence

    # For some character ch in sequence
    for i, ch in enumerate(sequence):
        # string containing all characters in sequence except ch
        rest = sequence[:i] + sequence[i+1:]
        
        # Each permutation of sequence is ch + a permutation of rest
        for perm in get_permutations(sequence[:i] + sequence[i+1:]):
            permutations.append(ch + perm)

    return permutations



if __name__ == '__main__':
    # Put three example test cases here (for your sanity, limit your inputs
    # to be three characters or fewer as you will have n! permutations for a 
    # sequence of length n)

    example_inputs = ['xy', 'abc', '312']
    example_outputs = [
        ['xy', 'yx'],
        ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'],
        ['123', '132', '213', '231', '312', '321']
        ]

    for example_input, output in zip(example_inputs, example_outputs):
        print('Input:', example_input)
        print('Expected Output:', output)

        permutations = get_permutations(example_input)

        print('Actual Output:', permutations)

        if sorted(permutations) == sorted(output):
            print('Correct')
        else:
            print('Incorrect')

        print('-' * 20)
