from hater import _joints
from hater import _frames
import os

class Reader (
	_joints.Reader,
	_frames.Reader
) :
	def __init__ ( self, input_file_path ) :
		self.input_file = open ( os.path.expandvars ( input_file_path ) )
		_joints.Reader.__init__ ( self )

	def load ( self ) :
		_joints.Reader.load ( self )
		_frames.Reader.load ( self )

class Manager (
	_joints.Reader,
	_frames.Reader,
	_frames.Writer
) :
	def __init__ ( self, input_file_path, output_file_path ) :
		self.input_file_path = input_file_path
		self.output_file_path = output_file_path
		_joints.Reader.__init__ ( self )

	def load ( self ) :
		self.input_file = open ( os.path.expandvars ( self.input_file_path ) )
		_joints.Reader.load ( self )
		_frames.Reader.load ( self )
		self.input_file.close (  )

	def write ( self ) :
		self.output_file = open ( os.path.expandvars ( self.output_file_path ), 'w' )
		_frames.Writer.write ( self )
		self.output_file.close (  )



class Tester :
	def test_load ( self ) :
		# Arrange
		r = Reader ( "$BVH_UTILS_PATH/tesset/input/short_reference.bvh" )
		# Act
		r.load (  )
		r.input_file.close (  )
		# Assert
		assert ( r.frame_count == 2 )
		assert ( len ( r.frames ) == 2 )
		assert ( len ( r.frames[0] ) == len ( r.joints ) )
		assert ( r.frames[0]['root']['position'][0] == 0.5909 )
		assert ( r.frames[1]['lhip']['rotation'][2] == -9.1346 )

	def test_write ( self ) :
		# Arrange
		output_file_path = "$BVH_UTILS_PATH/tesset/output/short_reference.bvh"
		m = Manager (
			"$BVH_UTILS_PATH/tesset/input/short_reference.bvh",
			output_file_path
		)
		# Act
		m.load (  )
		m.write (  )
		# Assert
		with open ( os.path.expandvars ( output_file_path ) ) as output_file :
			assert ( len ( output_file.readlines (  ) ) == 5 )

