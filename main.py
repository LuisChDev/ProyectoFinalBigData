import scrape
import prepro

u1 = 'cedemocratico'
filedir_ = u1
localfiles_ = True

# wrapping in a function


def main(partido=u1, filedir=u1, localfiles=True):
    if not localfiles:
        dir = scrape.scrapecomp(partido)
    else:
        dir = prepro.readlocal(partido)

    dset = prepro.get_files(dir, filedir)
    return dset
