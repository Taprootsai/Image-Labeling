# from pipeline import Pipeline
import argparse
# from ast import parse
import sys
import json
from pipeline import Pipeline
def parse_metadata():
    metadata = json.load(open('.metadata.json'))
    available_algorithms = 'Available plugins:\n'
    output = available_algorithms
    for plugin in metadata.get("plugins"):
        output += '\t\t' + "-"+plugin+"\n"
    
    available_selection_algorithms = metadata.get('selection_algorithms')

    output_selection_algo = 'Available selection Algotithms:\n'
    for algorithm in available_selection_algorithms:
        output_selection_algo += '- '+ algorithm +': '+available_selection_algorithms[algorithm]['description']
    
    return output + '\n\n' + output_selection_algo


if __name__=="__main__":
    availabel_args = {}
    availabel_args['--help'] = parse_metadata()

    if len(sys.argv) >= 2 :
        for i in range(1,len(sys.argv)):
            print('\n')
            print(availabel_args[sys.argv[i]])

    else:
        p = Pipeline()
        p.start_bucketizing()