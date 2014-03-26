# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 12:55:24 2013

@author: rik
"""

outdoc = html.tostring(h)

outdoc = outdoc.replace('\n', ' ')
outdoc = outdoc.replace('\t', ' ')
outdoc = outdoc.replace('<div', '\n <div')
outdoc = outdoc.replace('<em><i>', ' <em>')
outdoc = outdoc.replace('</i></em>', '</em> ')

def main():
    """main"""
    usage = "usage: %prog [args] arg"
    parser = ArgumentParser(usage)
    parser.add_argument("-r", "--recurse", dest="recurse", action="store_true",
                      help="""clean all files""")
    parser.add_argument("-f", "--filename", dest="filename",
                      help="specify csv filename as input")
    parser.add_argument("-b", "--basedir", dest="basedir",
                        help="specify basic directory")
    parser.add_argument("-o", "--outdir", dest="outdir",
                        help="specify destination directory")
    parser.add_argument("-x", "--outfile", dest="outfile",
                      help="""destination filename""")
    parser.add_argument("-s", "--soup", dest="soup", action="store_true",
                      help="""destination filename""")
                      
                    
    

    args = parser.parse_args()
        
    
    
    if not args.basedir:
        args.basedir = "."

    if not args.outdir or args.outdir=="":
        args.outdir = "."
    
    if args.recurse:
       recurse(basedir=args.basedir, 
                outdir=args.outdir)
    else:
        infile = os.path.join(args.basedir, args.filename)
        outfile = os.path.join(args.outdir, args.outfile)
        if args.soup == True:
            cleaner(infile, outfile, soup=True)
        else:
            cleaner(infile, outfile, soup=False)           
        

if __name__ == "__main__":
    main()