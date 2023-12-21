Function Lev_distance(a, b):
    let n be size of a
    let m be size of m
    let OPT be m x n matrix

    set OPT[i, 0] = i for i in range 0 ... m
    set OPT[0, j] = j for j in range 1 ... n

    for i in range 1 ... m:
        for j in range 1 ... n:
            diff = 0 if a[i] = b[j] else 1
            OPT[i,j] = Min { 1 + OPT[i-1, j], 1 + OPT[i, j-1], diff + OPT[i-1, j-1]}
    return OPT[m,n] # bottom right corner cell of the OPT matrix