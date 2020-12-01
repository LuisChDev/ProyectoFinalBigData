import scrape
import prepro

u1 = 'ceDemocratico'
filedir = u1
localfiles = False

if localfiles == False:
    dir = scrape.scrapecomp(u1)
else:
    dir = prepro.readlocal(u1)
#print(dir)
dset = prepro.get_files(dir, filedir)
print(dset)

