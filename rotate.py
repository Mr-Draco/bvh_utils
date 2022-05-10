from hater import Manager
from common.utils import load_environment_variables
import argparse

load_environment_variables (  )

parser = argparse.ArgumentParser (  )
parser.add_argument ( "input_file_path" )
parser.add_argument ( "output_file_path" )
args = parser.parse_args (  )

m = Manager ( args.input_file_path, args.output_file_path )
m.load (  )
m.rotate ( [ 90, 0, 0 ] )
m.write (  )
