from stemmer import stem
from tokenizer import tokenize_words, tokenize_sentences

print(list(tokenize_words("Hello, world!"))) # ["Hello", "world"]
print(list(tokenize_sentences("See Jack run. See jack play."))) # ["See Jack run.", "See Jack play"]

#
# Stemmer
#
# Offers a Porter Stemmer
#
print(list(map(stem, tokenize_words("I am going to the store does yourself want something?"))))
# ['I', 'go', 'store', 'want', 'someth', '?']