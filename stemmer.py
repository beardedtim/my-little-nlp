#
# All work is based off this document
#
# http://snowball.tartarus.org/algorithms/porter/stemmer.html
#
# The first part of the algorithm talks about
# what a constant is. So let's encode that in
# python!

# The following are _always_ considered
# vowels
always_vowels = ['a', 'e', 'i', 'o', 'u']

# given an index and a word


def is_constant(index, word):
  # if it is a vowel, return false
  if word[index] in always_vowels:
    return False
  # if it is the last letter and not
  # a vowel, return true
  if index == len(word) - 1:
    return True
  # Return true if it is not the letter y
  # or if it is the letter y and the next
  # letter is not a vowel
  # else it is not a constant
  return word[index] != 'y' or word[index + 1] not in always_vowels

# Any letter that is not a constant
# is a vowel


def is_vowel(index, word):
  return not is_constant(index, word)

# Given a dict of rules and a word to check
# if any stems match, apply the rule if
# the predicate function returns true


def format_by_rules(rules, word, fn=lambda a: True):
  # We want to only worry about the first one that
  # matches but specifically starting with the longest
  # one
  for key in sorted(rules, key=len, reverse=True):
    ending = word[-1 * len(key):]
    stem = word[:-1 * len(key)]
    if ending == key and fn(stem):
      return stem + rules[key]
  return word

# A sequence is a `c..v..` sequence
# of characters per the algo


def get_sequence(stem):
  seq = ""
  for i in range(len(stem)):
      if is_constant(i, stem):
          seq += 'c'
      else:
          seq += 'v'
  return seq

# the m or Measure is the count
# of `vc` sequences inside of our
# sequence of `c..v..c` characters


def get_stem_measure(stem):
  seq = get_sequence(stem)
  return seq.count('vc')


step_1_a_mappers = {
    'sses': 'ss',
    'ies': 'i',
    'ss': 'ss',
    's': ''
}


def step_1_a(word):
  return format_by_rules(step_1_a_mappers, word)


def has_eed_but_not_at_beginning(word):
  if word[-3:] == "eed":
    if get_stem_measure(word[:-3]) > 0:
      return word[:-3] + "ee"
  return word


def stem_contains_vowel(stem):
  for i, _ in enumerate(stem):
    if is_vowel(i, stem):
      return True

  return False


def ends_in_ed_with_a_vowel_in_stem(word):
  ending = word[-2:]
  if stem_contains_vowel(word[:-2]) and ending == "ed":
    return word[:-2]
  return word


def ends_in_ing_with_a_vowel_in_stem(word):
  ending = word[-3:]
  if stem_contains_vowel(word[:-3]) and ending == "ing":
    return word[:-3]
  return word


def add_e_to_at_ending(word):
  if word[-2:] == "at":
    return word + "e"
  return word


def add_e_to_bl_ending(word):
  if word[-2:] == "bl":
    return word + "e"
  return word


def add_e_to_iz_ending(word):
  if word[-2:] == "iz":
    return word + "e"
  return word


def double_constant_to_single(stem):
  ending = stem[-2:]
  if ending[0] == ending[1]:
    if ending == "ll" or ending == "ss" or ending == "zz":
      return stem
    return stem[:-1]
  return stem


def cvc_and_not_special_char(stem):
  ending = stem[-3:]
  ending_mapped = get_sequence(ending)
  return (ending_mapped == "cvc"
          and ending[2] != 'w'
          and ending[2] != 'x'
          and ending[2] != 'y')


def cvc_transform(stem):
  if cvc_and_not_special_char(stem) and get_stem_measure(stem) == 1:
    return stem + "e"
  return stem


def step_1_b(word):
  main_transformations = [
      has_eed_but_not_at_beginning,
      ends_in_ed_with_a_vowel_in_stem,
      ends_in_ing_with_a_vowel_in_stem
  ]

  sub_transformations = [
      add_e_to_at_ending,
      add_e_to_bl_ending,
      add_e_to_iz_ending,
      double_constant_to_single,
      cvc_transform
  ]

  def transform_again(w2):
    newWord = w2
    for fn in sub_transformations:
      newWord = fn(newWord)
    return newWord

  for i, fn in enumerate(main_transformations):
    newWord = fn(word)
    if newWord != word:
      if i == 0:
        return newWord
      return transform_again(newWord)
  return word


def step_1_c(word):
  if stem_contains_vowel(word) and word[-1] == 'y':
    return word[:-1] + 'i'
  return word


step_2_mapper = {
    'ational': 'ate',
    'tional': 'tion',
    'enci': 'ence',
    'anci': 'ance',
    'izer': 'ize',
    'abli': 'able',
    'alli': 'al',
    'entli': 'ent',
    'eli': 'e',
    'ousli': 'ous',
    'ization': 'ize',
    'ation': 'ate',
    'alism': 'al',
    'iveness': 'ive',
    'fulness': 'ful',
    'aliti': 'al',
    'iviti': 'ive',
    'biliti': 'ble'
}


def step2(word):
  return format_by_rules(
      step_2_mapper,
      word,
      lambda stem: get_stem_measure(stem) > 0
  )


step_3_mapper = {
    'icate': 'ic',
    'ative': '',
    'alize': 'al',
    'iciti': 'ic',
    'ical': 'ic',
    'ful': '',
    'ness': ''
}


def step3(word):
  return format_by_rules(
      step_3_mapper,
      word,
      lambda stem: get_stem_measure(stem) > 0
  )


def step4(word):
  removal_endings = [
      "al",
      "ance",
      "er",
      "ic",
      "able",
      "ible",
      "ant",
      "ement",
      "ence",
      "ment",
      "ent",
      "ou",
      "ism",
      "ate",
      "iti",
      "ous",
      "ive",
      "ize"

  ]
  newWord = ""
  # longest above is 5
  if word[-5:] in removal_endings:
    newWord = word[:-5]

  if len(newWord) == 0 and word[-4:] in removal_endings:
    newWord = word[:-4]

  if len(newWord) == 0 and word[-3:] in removal_endings:
    newWord = word[:-3]

  # ion is special!
  if word[-3:] == 'ion':
    if (
        word[-4] == "s"
        or word[-4] == "t"
    ):
      newWord = word[:-3]

  if word[-2:] in removal_endings:
    newWord = word[:-2]

  if get_stem_measure(newWord) > 1:
    return newWord
  return word


def step5a(word):
  measure = get_stem_measure(word[:-1])
  if word[-1] == 'e' and measure > 1:
    return word[:-1]

  if measure == 1 and not cvc_and_not_special_char(word[:-1]) and word[-1] == "e":
    return word[:-1]

  return word


def step5b(word):
  if word[-2:] == "ll" and get_stem_measure(word) > 1:
    return word[:-2] + "l"

  return word


def stem(word, debug=False):
  result = step_1_a(word.lower())
  if debug:
    print(result, "AFTER STEP 1a")

  result = step_1_b(result)
  if debug:
    print(result, "AFTER STEP 1b")

  result = step_1_c(result)
  if debug:
    print(result, "AFTER STEP 1c")

  result = step2(result)
  if debug:
    print(result, "AFTER STEP 2")

  result = step3(result)
  if debug:
    print(result, "AFTER STEP 3")

  result = step4(result)
  if debug:
    print(result, "AFTER STEP 4")

  result = step5a(result)
  if debug:
    print(result, "AFTER STEP 5a")

  result = step5b(result)
  if debug:
    print(result, "AFTER STEP 5b")

  return result


# def test_stemmer(debug=False):
#   # list taken from
#   # http://snowball.tartarus.org/algorithms/english/stemmer.html
#   stems = {
#       "consign": ["consign",
#                   "consigned",
#                   "consigning",
#                   "consignment"],

#       "consist": ["consist",
#                   "consisted",
#                   "consistency",
#                   "consistent",
#                   "consistently",
#                   "consisting",
#                   "consists"],
#       "consol": ["console",
#                  "consolation",
#                  "consolations",
#                  "console",
#                  "consoled",
#                  "consoles",
#                  "consoling",
#                  # "consolingly" this is in the list but
#                  # if you try nltk, it returns what our
#                  # algo returns
#                  "consols"
#                  ],
#       "consolatori": ["consolatory"],
#       "consolid": ["consolidate",
#                    "consolidated",
#                    "consolidating"]
#   }

#   for stem in stems:
#     words = stems[stem]
#     for word in words:
#       attempt = stemmer(word, debug)
#       if attempt != stem:
#         print(attempt, "attempt", stem, "stem")
#         return "I HAVE FAILED YOU!"
#   return "I HAVE SUCCEEDED"


# # You can pass in a debug flag, set to false
# # to keep it from printing the intermediary results
# # test_stemmer(debug=True)
# test_stemmer()