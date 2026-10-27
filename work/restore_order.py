from pathlib import Path
p=Path('work/lyrics')
def save(key,order):
    rows=[line.split('\t')[0] for line in (p/(key+'.tsv')).read_text().splitlines()]
    (p/(key+'.txt')).write_text('\n'.join(rows[i-1] if i else '' for i in order)+'\n')
save('casket-girl',[1,2,2,4,2,3,5,6,7,8,9,10,11,12,13,14,9,15,16,17,18,19,20,21,22,2,2,23,24,25,26,27,28,29,9,10,11,12,13,14,9,15,30,17,18,19,31,32,33,34,35,36,37,33,38,39,40,40,40,41])
save('its-alright',list(range(1,16))*2)
save('i-need-u-back',[1,2,3,4,5,6,7,8,0,9,10,11,12,0,13,14,13,15,0,16,17,0,18,19,20,0,9,10,11,12,21,0,22,23,24,15,0,16,17,16,17,25,26,25,27])
