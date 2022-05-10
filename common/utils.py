import os

ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)))

def load_environment_variables (  ) :
	from dotenv import load_dotenv
	ENV_PATH = os.path.join(ROOT, '.env')
	load_dotenv(ENV_PATH)

def translate_to_string ( vector ) :
	return ( ' '.join ( map ( str, vector ) ) )
