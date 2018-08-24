import string
import os

def get_column_widths(header, table):
    sizes = []
    for h in header:
        sizes.append(len(h))
    for row in table:
        for j, v in enumerate(row):
            if len(v) > sizes[j]:
                sizes[j] = len(v)
    return sizes

def as_markdown(header, table):
    maxSize = get_column_widths(header, table)
    lines = []
    lines.append(' | '.join([v.rjust(maxSize[i]) for i, v in enumerate(header)]))
    lines.append('-|-'.join(['-'*size for size in maxSize]))
    for row in table:
        lines.append(' | '.join([v.rjust(maxSize[i]) for i, v in enumerate(row)]))
    return os.linesep.join(lines)
    
def as_rst(header, table):
    maxSize = get_column_widths(header, table)
    lines = []
    lines.append('+-' + '-+-'.join(['-'*size for size in maxSize]) + '-+')
    lines.append('| ' + ' | '.join([v.rjust(maxSize[i]) for i, v in enumerate(header)]) + ' |')
    lines.append('+=' + '=+='.join(['='*size for size in maxSize]) + '=+')
    for row in table:
        lines.append('| ' + ' | '.join([v.rjust(maxSize[i]) for i, v in enumerate(row)]) + ' |')
        lines.append('+-' + '-+-'.join(['-'*size for size in maxSize]) + '-+')
    return os.linesep.join(lines)

def as_csv(header, table):
    lines = []
    lines.append(','.join(header))
    for row in table:
        lines.append(','.join(row))
    return os.linesep.join(lines)