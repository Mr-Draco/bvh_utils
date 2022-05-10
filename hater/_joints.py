from common.utils import translate_to_string
import numpy

class Writer :
	output_file = None
	joints = None

	def write ( self ) :
		self.depth = 0
		self.output_file.write ( "HIERARCHY\n" )
		self.output_file.write ( f"ROOT { self.joints[0]['name'] }\n" )
		self.write_joints ( self.joints[0] )

	def write_joints ( self, joint ) :
		self.output_file.write ( ( "\t" * self.depth ) + ( "{\n" ) )
		self.depth += 1
		self.output_file.write (
			( "\t" * self.depth ) + "OFFSET" + " " +
			translate_to_string ( joint["offset"] ) + "\n"
		)
		self.output_file.write (
			( "\t" * self.depth ) + "CHANNELS" + " " +
			str ( len ( joint["channels"] ) ) + " " +
			translate_to_string ( joint["channels"] ) + "\n"
		)
		for child in joint['children'] :
			self.output_file.write (
				( "\t" * self.depth ) + f"JOINT { child['name'] }\n"
			)
			self.write_joints ( child )
		self.depth -= 1
		self.output_file.write ( ( "\t" * self.depth ) + ( "}\n" ) )

class Reader :
	input_file = None
	def __init__ ( self ) :
		self.joints = []

	def load ( self ) :
		self.joint_stack = []
		self.channels_count = 0
		self.read_hierarchy (  )
		self.load_root (  )
		self.load_joints (  )

	def read_hierarchy ( self ) :
		self.input_line = self.input_file.readline ( ).split (  )
		assert ( self.input_line [ 0 ].lower (  ) == 'hierarchy' )

	def load_root ( self ) :
		self.input_line = self.input_file.readline ( ).split (  )
		assert ( self.input_line [ 0 ].lower (  ) == 'root' )
		joint = self.read_joint ( self.input_line [ 1 ].lower (  ) )
		joint['parent'] = None
		joint["children"] = []
		self.joints.append ( joint )
		self.joint_stack.append ( joint )

	def load_joints ( self ) :
		if ( not self.joint_stack ) :
			return
		self.input_line = self.input_file.readline ( ).split (  )
		if ( self.input_line [ 0 ].lower (  ) == 'joint' ) :
			joint = self.read_joint ( self.input_line [ 1 ].lower (  ) )
			joint['parent'] = self.joint_stack[-1]
			joint["children"] = []
			self.joints.append ( joint )
			self.joint_stack[-1]['children'].append ( joint )
			self.joint_stack.append ( joint )
			self.load_joints (  )
		elif ( self.input_line [ 0 ].lower (  ) == 'end' ) :
			# IGNORE END SITE SET
			self.input_file.readline (  )
			self.input_file.readline (  )
			self.input_file.readline (  )
			self.input_file.readline (  )
			self.current_joint = self.joint_stack.pop (  )
			self.load_joints (  )
		elif ( self.input_line [ 0 ].lower (  ) == '}' ) :
			self.current_joint = self.joint_stack.pop (  )
			self.load_joints (  )
		else :
			raise Exception("Expected token 'joint', 'end' or '}'")

	def read_joint ( self, name ) :
		self.input_line = self.input_file.readline ( ).split (  )
		assert ( self.input_line [ 0 ] == '{' )
		joint = { }
		joint["name"] = name
		self.input_line = self.input_file.readline ( ).split (  )
		assert ( self.input_line [ 0 ].lower (  ) == 'offset' )
		joint["offset"] = numpy.array ( [
			float ( self.input_line [ 1 ] ),
			float ( self.input_line [ 2 ] ),
			float ( self.input_line [ 3 ] )
		] )
		self.input_line = self.input_file.readline ( ).split (  )
		assert ( self.input_line [ 0 ].lower (  ) == 'channels' )
		assert ( self.input_line [ 1 ].isdigit (  ) )
		self.channels_count += int ( self.input_line [ 1 ] )
		joint["channels"] = []
		for index in range ( int ( self.input_line [ 1 ] ) ) :
			joint["channels"].append ( self.input_line [ index + 2 ].lower (  ) )
		return joint

class Manager (
	Writer,
	Reader
):
	joints = None
	def __init__ ( self ) :
		Reader.__init__ ( self )

	def scale ( self, value ) :
		for joint in self.joints :
			joint["offset"] = joint["offset"] * value
