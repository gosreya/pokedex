"""This algorithm is a version of the spelling-corrector written by Peter Norvig presented in this http://www.norvig.com/spell-correct.html. The original probability function has been modified, as this spelling-corrector is aimed to identify names rather than natural language words."""

CONSONANTS = {
  "a", "b", "c", "d", "f", 
  "g", "h", "j", "k", "l", 
  "m", "n", "p", "q", "r", 
  "s", "t", "v", "w", "x",
  "y", "z"
}

"""
Areas for improvement: 
- Increase points for proximity of the consonants to where they were in the original word. 
- Account for common errors such as s/c replacement. 
- Address the impossibility of finding the correction for an input thats incorrect by more than 2 letters.
"""
class SpellCorrector:
  def __init__(self, word_list):
    self.dictionary = word_list

  def P(self, og, suggestion): 
      """Probability that `suggestion` is what the userintended. Here, I assume that the user is likelier to get the consonants of the name more correctly than the vowels, so I give more weight to the suggestions with the same consonants.
      """
      consonant_matching = 1
      for letter in suggestion:
        if (letter in CONSONANTS) and (letter in og):
          consonant_matching += 1
      return consonant_matching
    

  def correction(self, word): 
      """Most probable spelling correction for word."""
      return max(self.candidates(word), key=lambda x : self.P(word, x))
  
  def candidates(self, word): 
      """Generate possible spelling corrections for word."""
      return (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])
  
  def known(self, words): 
      """The subset of `words` that appear in the dictionary of POKEMON."""
      return set(w for w in words if w in self.dictionary)
  
  def edits1(self, word):
      """All edits that are one edit away from `word`."""
      letters    = 'abcdefghijklmnopqrstuvwxyz'
      splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
      deletes    = [L + R[1:]               for L, R in splits if R]
      transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
      replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
      inserts    = [L + c + R               for L, R in splits for c in letters]
      return set(deletes + transposes + replaces + inserts)
  
  def edits2(self, word): 
      """All edits that are two edits away from `word`."""
      return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))
