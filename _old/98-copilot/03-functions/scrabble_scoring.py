def num_points(word):
    """
    Each letter is worth the following points:
    a, e, i, o, u, l, n, s, t, r: 1 point
    d, g: 2 points
    b, c, m, p: 3 points
    f, h, v, w, y: 4 points
    k: 5 points
    j, x: 8 points
    q, z: 10 points
    word is a word consisting of lowercase characters.
    Return the sum of points for each letter in word.
    """
    points = {
    'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1, 'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
    'd': 2, 'g': 2,
    'b': 3, 'c': 3, 'm': 3, 'p': 3,
    'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
    'k': 5,
    'j': 8, 'x': 8,
    'q': 10, 'z': 10
    }
    return sum(points[letter] for letter in word)

def best_word(word_list):
           """
           word_list is a list of words.
           Return the word worth the most points.
           """
           return max(word_list, key=num_points)

if __name__ == '__main__':
        
    # word = input("Enter a word: ")
    # print(f"The total score for {word} is {num_points(word)}")

    word_list = ['hello', 'world', 'python', 'is', 'awesome']
    # generate the list of scores for each word in word_list
    scores = [num_points(word) for word in word_list]
    # print words and their scores in one line
    print(' '.join([f"'{word}': {score}" for word, score in zip(word_list, scores)]))

    print(f"The word worth the most points is: '{best_word(word_list)}' with score: {num_points(best_word(word_list))}")

    # print "This is the end of chapter 3" in the next line
    print("This is the end of chapter 3")