#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cube PhaseChange
Dennis Svatunek
2018
UCLA

dennis.svatunek@gmail.com
@clickchemist

Changes the phase in Gaussian cube files

Available options:

Change to opposite phase (standard)
Change all to positive (-p)
Change all to negative (-n)
Renumber the orbital numbers by adding 1000 (-c)

Please cite: http://doi.org/10.5281/zenodo.1472621
https://github.com/dsvatunek/cube_phasechange
"""
__version__= '1.0.0'

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def isFloat(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False


#checks if every element in list is an int    
def checklineint(line):
    x =True
    for element in line:
        if isInt(element):
            pass
        else:
            x = False
    return x

            
def main():
    import argparse
    import sys
    import time
    description="""
Cube PhaseChange
Dennis Svatunek
2018
UCLA

dennis.svatunek@gmail.com
@clickchemist

Changes the phase in Gaussian cube files

Available options:

Change to opposite phase (standard)
Change all to positive (-p)
Change all to negative (-n)
Renumber the orbital numbers by adding 1000 (-c)

Please cite: http://doi.org/10.5281/zenodo.1472621
https://github.com/dsvatunek/cube_phasechange
"""

    
    parser =  argparse.ArgumentParser(usage='%(prog)s [settings] inp_file',  description=description)
    parser.add_argument('inp_file', metavar='Input file', type=str, help='Name of the cube file')
    parser.add_argument('-n', action='store_true', default=False, help='Set everything to negative value')
    parser.add_argument('-p', action='store_true', default=False, help='Set everything to positive value')
    parser.add_argument('-c', action='store_true', default=False, help='Change orbital number in modified cube files. Eliminates problems with gaussview')
       
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)	
    args = parser.parse_args()
    
    starttime=time.time()
    input_object = open(args.inp_file, 'r')
    output_file = open(''.join(args.inp_file.split('.')[:-1])+'_modified.'+args.inp_file.split('.')[-1],'w')
    
    input_file = (line for line in input_object) #generator
    
    #skip first two lines
    output_file.write(next(input_file))
    output_file.write(next(input_file))

    
    #iter over lines until value matrix starts
    for line in input_file:
        if len(line.split())-1 == int(line.split()[0]) and checklineint(line.split()):
            if args.c:
                line = [int(x) for x in line.split()]
                line[1:] = [x+1000 for x in line[1:]]
                line = ['{:>5}'.format(str(x)) for x in line]
                output_file.write(''.join(line)+"\n")
            else:
                output_file.write(line)
            break
        else:
            output_file.write(line)
            pass
    
    if args.n:
        for line in input_file:
            values = line.split()
            for i in range(len(values)):
                if isFloat(values[i]):
                    if float(values[i]) > 0:
                        values[i] = float(values[i])*-1
                    else:
                        pass
                else:
                    sys.exit("Expected float, found other.")
            values = ['{:>13}'.format(str(x)) for x in values]
            output_file.write(''.join(values)+'\n')
    elif args.p:
        for line in input_file:
            values = line.split()
            for i in range(len(values)):
                if isFloat(values[i]):
                    if float(values[i]) < 0:
                        values[i] = float(values[i])*-1
                    else:
                        pass
                else:
                    sys.exit("Expected float, found other.")
            values = ['{:>13}'.format(str(x)) for x in values]
            output_file.write(''.join(values)+'\n')
    else:
        for line in input_file:
            values = line.split()
            for i in range(len(values)):
                if isFloat(values[i]):
                    values[i] = float(values[i])*-1
                else:
                    sys.exit("Expected float, found other.")
            values = ['{:>13}'.format(str(x)) for x in values]
            output_file.write(''.join(values)+'\n')
    
    output_file.close()
    
    endtime =time.time()
    totaltime=str(endtime-starttime)
    seconds=totaltime.split('.')[0]
    milliseconds=float('0.'+totaltime.split('.')[1])*1000
    print('Finished after {} seconds and {:.0f} ms\n'.format(seconds, float(milliseconds)))    
            

if __name__ == "__main__":
    main()
