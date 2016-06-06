import vk
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=vk.a_db)
#Session = sessionmaker(bind=vk.a_db)
#Session
session = Session()

a= session.query(vk.Persoon).order_by(vk.Persoon.gebjaar)
#a.count()


f = session.query(vk.Functies)
#f.count()

fn = session.query(vk.Functienaam)
#fn.count()


r = session.query(vk.Functies).first()

"""print 'dit is een functie'
print 'r:', r
print 'met, bv, een beginDag'
print 'r.beginDAg:', r.beginDag
print 'en ene relatie meet Functienaam'
print 'r.naam:', r.naam 
print 'r.naam.geslachtsnaam:', r.naam.naam"""
    
"""gbf = session.query(vk.Functies.functienaam,
                    vk.Functies.naam,
                    func.count(vk.Functies.functienaam)).group_by(vk.Functies.functienaam)
this goes wrong because it is a query, not a Function

print gbf.all()
"""

#this returns the right stuff

from collections import defaultdict

def vk_period((p1, p2)):
    t = f.filter(vk.Functies.beginJaar.between(p1, p2))
    x = t.group_by(vk.Functies.functienaam).add_column(func.count(vk.Functies.persoon).label("aantal"))
    y = x.order_by("aantal")
    return y


def vk_per_table(start, stop, interval):
    """returns defaultdictionary with number of vk per interval with start and end year"""
    d = defaultdict(defaultdict)
    for yrs in [(x,x+interval-1) for x in xrange(start, stop, interval)]:
        x = vk_period(yrs)
        for i, v in x.all():
            d['%s-%s' % yrs][i.naam.naam] = v
    return d

def vk_zpp((p1, p2)):
    """zittingsduur per periode"""
    res = f.filter(vk.Functies.beginJaar.between(p1, p2))
    x = res.filter(vk.Functies.eindJaar != None)
    return [float((item.eindJaar - item.beginJaar))+ 1.0/2 for item in x]

def average(l):
    return sum(l)/float(len(l))

def median(l):
    '''statistical median with '''
    copy = sorted(l)
    size = len(copy)
    if size % 2 == 1:
        return copy[(size - 1) / 2]
    else:
        return (copy[size/2 - 1] + copy[size/2]) / 2


def vk_zpp_table(start,stop, interval):
    """returns defaultdictionary with avg zittingsduur per periode"""
    d = defaultdict(defaultdict)
    for yrs in [(x, x+interval-1) for x in xrange(start, stop, interval)]:
        x = vk_zpp(yrs)
        for v in x:
            d['%s-%s' % yrs]['aant'] = len(x)
            d['%s-%s' % yrs]['avg'] = average(x)
            d['%s-%s' % yrs]['med'] = median(x)
            d['%s-%s' % yrs]['max'] = max(x)
            d['%s-%s' % yrs]['min'] = min(x)+1/2
            
    return(d)
           
def vk_table_as_csv(d=defaultdict, names=[], f='fl'):
    """this works with default names, because
    I can think of no other way to call them in the same order
    perhaps defaultdict supports this"""
    fl =  open(f, 'w')
    csvfl = UnicodeWriter(fl, encoding='cp1252')
    names.sort()
    csvfl.writerow(['']+names)
    vals = d.keys()
    vals.sort()
    for key in vals:
        out = d[key]
        oud = []
        oud.append('%s' % key)
        for n in names:
            try:
                oud.append(u'%s' % out[n])
            except KeyError:
                oud.append(u'0')
        csvfl.writerow(oud)
    fl.close()
    return '%s written' % f


#for item, count in y.all():
#    print item.naam.naam, count


import csv, codecs, cStringIO
class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self




class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)






