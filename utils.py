import re
import os
import numpy
import itertools

def vectorize_txts(txt_dir):
    vecs = {}
    for file in os.listdir(txt_dir):
        if file.endswith('.txt'):
            with open(os.path.join(txt_dir, file), 'rb') as f:
                vecs[os.path.splitext(file)[0]] = vectorize_txt(f.read())
    return vecs

def vectorize_txt(text, punc='!,.?;:'):
    """Converts given text to list of word counts between
       punctuation characters given as string punc

       Initial granularity is exactly as it comes in
    """
    split_by_punc = re.split('[%s]' % punc, text)
    excess = re.compile('([^\s\w]|_)+')
    split_by_punc = [excess.sub('', part) for part in split_by_punc]

    return [len(part.split()) for part in split_by_punc]

def collapse_vector(vec, lgth):
    """Collapses given vector to lgth (right now, minimum length of all
       vectorized texts in batch) by assigning
       floor(len(vec)/lgth)-sized pieces to lgth positions.

       Haven't decided what to do with the remainder...
    """
    collapsed = []
    part_lgth = len(vec)/lgth

    idx = 0
    for i in range(0, lgth):
        collapsed.append(numpy.mean(vec[idx:idx + part_lgth]))
        idx += part_lgth

    return collapsed

def calculate_similarity(vec, others):
    """Calculate and return cosine similarity between vec and arbitrary-length
       list of other vectors

       First, everything is collapsed to length of shortest vector
    """
    # eeewww
    min_lgth = min(itertools.chain([len(vec),], map(len, others)))
    vec = collapse_vector(vec, min_lgth)
    others = [collapse_vector(vect, min_lgth) for vect in others]

    sims = []
    magn = numpy.linalg.norm

    for other in others:
        dot = float(numpy.dot(vec, other))
        sim = dot / float(magn(vec) * magn(other))
        sims.append(sim)

    return sims
