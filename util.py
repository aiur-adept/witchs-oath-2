def in_rect(p, r):
    return p[0] >= r[0] and \
            p[0] < (r[0] + r[2]) and \
            p[1] >= r[1] and \
            p[1] < (r[1] + r[3])
