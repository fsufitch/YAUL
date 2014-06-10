import sys
from yaul import parallel

if len(sys.argv)<2:
    print("Please pass a text file as an argument.")
    sys.exit()

par_type = sys.argv[2] if len(sys.argv)>2 else None

while not par_type:
    for i, pt in enumerate(parallel.PARALLEL_TYPES):
        print("%s) %s" % (i, pt))
    try:
        typ_key = int(str(input("Parallel type? (by number) ")).strip())
        par_type = parallel.PARALLEL_TYPES[typ_key]
    except Exception:
        continue


def count_words(line):
    return len(line.split())
def sum_words(sums):
    return [sum(sums)]

pool = parallel.GenericPool(par_type)

with open(sys.argv[1]) as infile:
    data = pool.map_reduce(count_words, infile, reducer=sum_words)
    
print(list(data)[0])