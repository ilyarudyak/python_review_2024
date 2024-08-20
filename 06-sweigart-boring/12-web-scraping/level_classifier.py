"""
This script classifies the level of python books from Nostarch Press
based on their detailed description. It uses Zero-Shot Classification Pipeline
from the transformers library.
"""
import json
from transformers import pipeline

class LevelClassifier:

    BEGINNER = 'Beginner'
    INTERMEDIATE = 'Intermediate'
    THRESHOLD = 0.6

    def __init__(self, 
                 filename='nostarch_books_python.json'):
        self._books = self._load_books(filename)
        self._classifier = pipeline('zero-shot-classification', 
                                    model='facebook/bart-large-mnli',
                                    device=0)

    def _load_books(self, filename):
        with open(filename, 'r') as f:
            return json.load(f)
        
    def classify_books(self):
        for book in self._books:
            level, score = self._classify_book(book['full_description'])
            book['level'] = level
            book['score'] = score
            

    def _classify_book(self, description):
        candidate_labels=[self.BEGINNER, self.INTERMEDIATE]
        label, score = self._classifier(description, candidate_labels)['labels'][0], \
                       self._classifier(description, candidate_labels)['scores'][0]
        # Change label to INTERMEDIATE the score is below the threshold
        if score < self.THRESHOLD:
            label = self.INTERMEDIATE
            score = 1 - score

        # Format score to 2 decimal places
        score = round(score, 2)

        return label, score
    
    def save_books(self, output_file='nostarch_books_python_classified.json'):
        with open(output_file, 'w') as f:
            json.dump(self._books, f, indent=2)

if __name__ == '__main__':
    classifier = LevelClassifier()
    classifier.classify_books()
    classifier.save_books()