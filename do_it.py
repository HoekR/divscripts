from lxml import etree
import os, sys
import time
import re
SRC_DIR = os.path.join(os.path.abspath('.'), 'src')
DST_DIR = os.path.join(os.path.abspath('.'), 'dst')

SRC_PERSONEN =  'personen_index.txt'
SRC_ZAKEN = 'zaken_index.txt'


def is_letter(l, i):
    l = l.strip()
    if i == 0 and len(l) == 4 and l[-1] == 'A':
        return 'A' 
    if l and l in 'abcdefghijklmnopqrstuvwxyz'.upper() or l in ['IJ/Y']:
        #dit is een letter in het alfabet
        return l 
def convert_zaken():
    f = open(os.path.join(SRC_DIR, SRC_ZAKEN))
    out_f = open(os.path.join(DST_DIR, SRC_ZAKEN[:-4] + '.xml'), 'w')
    out_f.write('<groen_index>')    
    out_f.write('\n')
    out_f.write("""<comment>
        Zakenindex voor de "Groen" bestanden

        automatically generated %s 
        </comment>""" % time.ctime())
    out_f.write('\n')
    parse_file(f, out_f)
    
    out_f.write('</groen_index>')
    out_f.write('\n')
def convert_personen():
    f = open(os.path.join(SRC_DIR, SRC_PERSONEN))
    out_f = open(os.path.join(DST_DIR, SRC_PERSONEN[:-4] + '.xml'), 'w')
    out_f.write('<groen_index>')    
    out_f.write('\n')
    out_f.write("""<comment>
        Personenindex voor de "Groen" bestanden

        automatically generated %s 
        </comment>""" % time.ctime())
    out_f.write('\n')
    parse_file(f, out_f)

    out_f.write('</groen_index>')
    out_f.write('\n')

def parse_file(in_f, out_f):
    f = in_f
    i = 0
    for l in f.readlines():
        l = l.strip()
        orig_l = l
        tagged_l = ''
        if is_letter(l, i):
            tagged_l = '<letter>%s</letter> ' % is_letter(l, i)
        elif l:
            if l.startswith('*'):
                tagged_l += '<item starred="1">'
#                l = l[1:].strip()
                tagged_l += '* '
            else:
                tagged_l += '<item>'
            #the regel zou precies 1 voorkomen van een dubbele punt moeten bevatten
            #als scheiding tussen auteur en verwijzing
            #er is alleen 1 speciaal geval: in de zakenindex zijn er regel die met een jaartal beginnen, en die hebben wel een dubbele punt:
            tagged_l += parse_line(l, i)
        out_f.write(tagged_l)
        out_f.write('\n')
#        print tagged_l
        i+=1
#        if i > 10: return



def parse_line(l, i):
    tagged_l = ''
    #de naam hoeft verder niets mee te gebeuren
    #we willen de structuur van de oorspronkelijke tekst geheel bewaren
    #dus we lopen er lineair, van links naar rechts, doorheen:
    assert ':' in l, 'Verwachtte tenminste 1 dubbele punt in deze regel: %s: "%s"' % (i, l)
    #voor de ':' staat de naam, die zetten we in tagged
    tagged_l += '<naam>%s:</naam>' % l[:l.find(':')]
    l = l[l.find(':') + 1:]
#    l = l.strip()
 
    tagged_l += '<references>'
    #de verwijzing is *of* een zie-verwijzing, of het zijn delen en blznummers
    #strip the periode in the end (we add it again later to parsed_l)
    if l.endswith('.'):
        l = l[:-1]
    tagged_l += tag_pages(l, i)
    l + '.'
    tagged_l += '</references>'
    tagged_l += '</item>\n'
    return tagged_l

def tag_pages(l, i):
    orig_l = l
    result = ''
    deel_m, deel = find_deelnummer(l) 
    while deel_m:
        next_deel_m, next_deel = find_deelnummer(l[deel_m.end():])
#        print l[deel_m.end():]
        #determine the string to work on in this round
        if next_deel_m:
            s = l[:next_deel_m.start() + deel_m.end()]
            l = l[next_deel_m.start() + deel_m.end():]
        else:
            s = l
            l = ''
#        print '[found %s]' % deel
#        print 'working on %s' % s
#        print 'remaining string: %s'  % l
        if deel == 'zie':
            #als het een zieverwijzing betreft
            #pleuren we dehele string tussne <zie> en zijn we klar
            result += '%s<zie>%s</zie>' % (s[:deel_m.start()], s[deel_m.start():])
        else:
            #anders proberen we alle paginanummers te vinden
            #het deelnummer teggen we verder niet maar komt gewoonbij het resultaat
#            print 'result', result
#            print 'deel_m.end()', deel_m.end()
            begin_s = s[:deel_m.start()]
            if ':' in begin_s:
                result += '<naam>%s</naam>%s' % (begin_s[:begin_s.find(':')], begin_s[begin_s.find(':'):])
            else:
                result += begin_s 

            result += s[deel_m.start():deel_m.end()]
#            print 'result', result
            s = s[deel_m.end():]
#            print s
            m = re.search('[0-9]+', s)
            assert m, 'geen paginanummer op deze regel? %s: "%s"' % (i, l)
            while m:
                result += s[:m.start()]
                number = s[m.start():m.end()]
                result += '<page deel="%s" number="%s">%s</page>' % (deel, number, number)

                s = s[m.end():]
                m = re.search('[0-9]+', s)
            result += s

        deel_m, deel = find_deelnummer(l) 
    return result

def find_deelnummer(s):
    ls = [(re.search(s1, s), s2) for s1, s2 in [
        ('I, ', 'I'),
        ('II, ', 'II'),
        ('zie ', 'zie'),
        ('Zie ', 'zie'),
        ]]
    ls = [(m, x) for m, x in ls if m and (s[m.end()].isdigit() or x == 'zie')]
    ls = [(m.start(), (m, s)) for m,s in ls if m]
    if ls:
        i, result = min(ls)
        return result
    else:
        return None, None


def xxxparse_pages(l, i):
    orig_l = l
    result = ''
#    l = l.strip()
    assert l.startswith('I,') or l.startswith('II,'), \
        '%s: "%s" - %s' % (i,l, 'Expected this fragment to start with "I" or "II"')
    if l.startswith('I, '):
#        l = l[2:].strip()
        deel = 'I'
    else:
#        l = l[3:].strip()
        deel = 'II'
    while l:
        if l.find(',') > 0:
            nr = l[:l.find(',')]
            l = l[l.find(',') + 1:].strip()
        
        else:
            nr = l
            l = ''
        #\xe2 is een afbreekstreepje uit word
        if '\xe2' in nr:
            pagenr = nr.split('\xe2')[0]
        elif '-' in nr:
            pagenr = nr.split('-')[0]
        else:
            pagenr = nr

        if pagenr.endswith('?'):
            pagenr = pagenr[:-1]
        if '(' in pagenr:
            pagenr = pagenr[:pagenr.find('(')]
        pagenr = pagenr.strip()
        assert pagenr.isdigit(), '%s: "%s"' % (i, pagenr) + orig_l
        result += '<page deel="%s" n="%s">%s</page>, ' % (deel, pagenr, nr)
    
    return '%s, %s' % (deel, result)

if __name__ == "__main__":
    convert_personen()
    convert_zaken()

