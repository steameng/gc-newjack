from random import randint
import wave
#from scikits.audiolab import wavread, wavwrite
#from scipy import vstack



def randomizer(files):

    # Categorize Files
    intros = filter(lambda x: 'intro' in x.name, files)
    verses = filter(lambda w: 'verse' in w.name, files)
    bridges = filter(lambda z: 'bridge' in z.name, files)
    fillers = filter(lambda u: 'filler' in u.name, files)

    # Choose random file from list
    intro = intros[randint(0, len(intros) - 1)]
    verse = verses[randint(0, len(verses) - 1)]
    bridge = bridges[randint(0, len(bridges) - 1)]
    filler = fillers[randint(0, len(fillers) - 1)]

    # Group Files
    infiles = [intro, verse, filler, bridge]

    return infiles
