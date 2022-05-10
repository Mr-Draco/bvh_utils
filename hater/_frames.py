from scipy.spatial.transform import Rotation
import numpy

class Writer :
	frames = None
	frame_count = None
	frame_time = None
	joints = None
	output_file = None
	def write ( self ) :
		self.output_file.write ( "MOTION\n" )
		self.output_file.write ( f"FRAMES: { self.frame_count }\n" )
		self.output_file.write ( f"FRAME TIME: { self.frame_time }\n" )
		self.write_frames (  )

	def write_frames ( self ) :
		for frame in self.frames :
			self.write_frame ( frame )

	def write_frame ( self, frame ) :
		for joint in self.joints :
			self.write_joint ( joint, frame )
		self.output_file.write ( "\n" )

	def write_joint ( self, joint, frame ) :
		vector = numpy.array ( [ 0.0, 0.0, 0.0 ] )
		for channel in joint["channels"] :
			value = self.get_channel_value ( channel, joint, frame )
			self.output_file.write ( f"{ value } " )

	def get_channel_value ( self, channel, joint, frame ) :
			channel_axis = channel[0]
			channel_type = channel[1:]
			if ( channel_axis == 'x' ) :
				return ( frame[joint['name']][channel_type][0] )
			if ( channel_axis == 'y' ) :
				return ( frame[joint['name']][channel_type][1] )
			if ( channel_axis == 'z' ) :
				return ( frame[joint['name']][channel_type][2] )

class Reader :
	joints = None
	input_file = None
	input_line = None
	def compute_frame_vector ( self, channel_type, joint ) :
		# ASSUMES CHANNELS ARE GROUPED BY TYPE
		vector = [ 0.0, 0.0, 0.0 ]
		for channel in joint["channels"] :
			if ( channel.endswith ( channel_type ) ) :
				channel_axis = channel[0]
				if ( channel_axis == 'x' ) :
					vector[0] = float ( self.input_line [ self.input_line_word_index ] )
				elif ( channel_axis == 'y' ) :
					vector[1] = float ( self.input_line [ self.input_line_word_index ] )
				elif ( channel_axis == 'z' ) :
					vector[2] = float ( self.input_line [ self.input_line_word_index ] )
				self.input_line_word_index += 1
		return numpy.array ( vector )

	def load ( self ) :
		self.read_motion (  )
		self.load_frame_count (  )
		self.load_frame_time (  )
		self.load_frames (  )

	def read_motion ( self ) :
		self.input_line = self.input_file.readline ( ).split (  )
		assert ( self.input_line [ 0 ].lower (  ) == 'motion' )

	def load_frame_count ( self ) :
		self.input_line = self.input_file.readline ( ).split (  )
		assert ( self.input_line [ 0 ].lower (  ) == 'frames:' )
		assert ( self.input_line [ 1 ].isdigit (  ) )
		self.frame_count = int ( self.input_line [ 1 ] )

	def load_frame_time ( self ) :
		self.input_line = self.input_file.readline ( ).split (  )
		assert ( self.input_line [ 0 ].lower (  ) == 'frame' )
		assert ( self.input_line [ 1 ].lower (  ) == 'time:' )
		assert ( self.input_line [ 2 ].replace ( '.', '', 1 ).isdigit (  ) )
		self.frame_time = float ( self.input_line [ 2 ] )

	def load_frame ( self ) :
		self.input_line_word_index = 0
		frame = {}
		for joint in self.joints :
			frame[joint["name"]] = {}
			frame[joint["name"]]["position"] = (
				self.compute_frame_vector ( "position", joint )
			)
			frame[joint["name"]]["rotation"] = (
				self.compute_frame_vector ( "rotation", joint )
			)
		# THE FOLLOWING ASSERT
			# NOT THE MOST EFFICIENT BUT WHO CARES
			# IF THERE IS AN ERROR THEN ALL LOADED DATA IS LOST
		assert ( len ( self.input_line ) == self.input_line_word_index )
		return frame

	def load_frames ( self ) :
		self.frames = []
		self.input_line = self.input_file.readline ( ).split (  )
		while ( self.input_line ) :
			self.frames.append (
				self.load_frame (  )
			)
			self.input_line = self.input_file.readline ( ).split (  )

class Manager (
	Writer,
	Reader
):
	frames = None
	def rotate ( self, rotation_vector ) :
		r = Rotation.from_rotvec ( rotation_vector, degrees = True )
		for frame in self.frames :
			root = frame[ list ( frame.keys (  ) )[0] ]
			root['position'] = r.apply ( root['position'] )
			for joint in frame.keys (  ) :
				if ( 'rotation' in frame[joint] ) :
					frame[joint]['rotation'] = r.apply ( frame[joint]['rotation'] )

	def scale ( self, value ) :
		for frame in self.frames :
			for joint in frame.keys (  ) :
				if ( 'position' in frame[joint] ) :
					frame[joint]['position'] = frame[joint]['position'] * value
