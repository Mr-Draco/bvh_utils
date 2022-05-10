from hater import _frames
from hater import _joints
import os

class Writer (
	_joints.Writer,
	_frames.Writer
):
	joints = None
	frames = None
	def __init__ ( self, output_file_path ) :
		self.output_file_path = output_file_path

	def write ( self ) :
		self.output_file = open ( os.path.expandvars ( self.output_file_path ), 'w' )
		_joints.Writer.write ( self )
		_frames.Writer.write ( self )
		self.output_file.close (  )


class Reader (
	_joints.Reader,
	_frames.Reader
) :
	def __init__ ( self, input_file_path ) :
		self.input_file_path = input_file_path
		_joints.Reader.__init__ ( self )
		_frames.Reader.__init__ ( self )

	def load ( self ) :
		self.input_file_line_index = 0
		self.input_file = open ( os.path.expandvars ( self.input_file_path ) )
		_joints.Reader.load ( self )
		_frames.Reader.load ( self )
		self.input_file.close (  )

class Manager (
	Reader,
	Writer
):
	def __init__ ( self, input_file_path, output_file_path ) :
		Reader.__init__ ( self, input_file_path )
		Writer.__init__ ( self, output_file_path )

	def rotate ( self, rotation_vector ) :
		_frames.Manager.rotate ( self, rotation_vector )

	def scale ( self, value ) :
		_joints.Manager.scale ( self, value )
		_frames.Manager.scale ( self, value )

