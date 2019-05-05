from functools import reduce
import re

stop_words = [
    "i",
    "me",
    "my",
    "myself",
    "we",
    "our",
    "ours",
    "ourselves",
    "you",
    "your",
    "yours",
    "yourself",
    "yourselves",
    "he",
    "him",
    "his",
    "himself",
    "she",
    "her",
    "hers",
    "herself",
    "it",
    "its",
    "itself",
    "they",
    "them",
    "their",
    "theirs",
    "themselves",
    "what",
    "which",
    "who",
    "whom",
    "this",
    "that",
    "these",
    "those",
    "am",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "having",
    "do",
    "does",
    "did",
    "doing",
    "a",
    "an",
    "the",
    "and",
    "but",
    "if",
    "or",
    "because",
    "as",
    "until",
    "while",
    "of",
    "at",
    "by",
    "for",
    "with",
    "about",
    "against",
    "between",
    "into",
    "through",
    "during",
    "before",
    "after",
    "above",
    "below",
    "to",
    "from",
    "up",
    "down",
    "in",
    "out",
    "on",
    "off",
    "over",
    "under",
    "again",
    "further",
    "then",
    "once",
    "here",
    "there",
    "when",
    "where",
    "why",
    "how",
    "all",
    "any",
    "both",
    "each",
    "few",
    "more",
    "most",
    "other",
    "some",
    "such",
    "no",
    "nor",
    "not",
    "only",
    "own",
    "same",
    "so",
    "than",
    "too",
    "very",
    "s",
    "t",
    "can",
    "will",
    "just",
    "don",
    "should",
    "now"
]


def remove_stop_words(words):
  return filter(lambda word: not word in stop_words, words)


def clean_words(word):
  return re.sub(
              pattern=r'(\,|\.|\?|\!|\'|\;|\:)',
              repl=' \\1',
              string=word
          )


def tokenize_words(phrase):
  clean_phrase = clean_words(phrase)
  words = clean_phrase.split()
  filtered = remove_stop_words(words)

  return filtered


def tokenize_sentences(phrase):
  reg = re.compile(r'(\.|\?|\!)')
  with_tokens = reg.split(phrase)
  sentences = []
  last_sentence = ""
  for value in with_tokens:
    if reg.match(value):
      sentences.append(last_sentence + value)
      last_sentence = ""
    else:
      last_sentence += value
  # If we have any left overs, someone didn't complete
  # their sentence!
  if len(last_sentence):
    # let's append it as our last value!
    sentences.append(last_sentence)

  return filter(lambda l: len(l), sentences)