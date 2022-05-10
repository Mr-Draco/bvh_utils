from hater import _joints
import os

class Reader ( _joints.Reader ) :
	def __init__ ( self, input_file_path ) :
		self.input_file = open ( os.path.expandvars ( input_file_path ) )
		_joints.Reader.__init__ ( self )

class Manager (
	_joints.Reader,
	_joints.Writer
) :
	def __init__ ( self, input_file_path, output_file_path ) :
		self.input_file_path = input_file_path
		self.output_file_path = output_file_path
		_joints.Reader.__init__ ( self )

	def load ( self ) :
		self.input_file = open ( os.path.expandvars ( self.input_file_path ) )
		_joints.Reader.load ( self )
		self.input_file.close (  )

	def write ( self ) :
		self.output_file = open ( os.path.expandvars ( self.output_file_path ), 'w' )
		_joints.Writer.write ( self )
		self.output_file.close (  )


class Tester :
	def test_load ( self ) :
		# Arrange
		r = Reader ( "$BVH_UTILS_PATH/tesset/input/t_pose.bvh" )
		# Act
		r.load (  )
		r.input_file.close (  )
		# Assert
		assert ( len ( r.joints ) == 20 )
		assert ( r.channels_count == 63 )
		assert ( not ( r.joint_stack ) )
		assert ( r.joints[0]["name"] == "root" )
		assert ( r.joints[0]["parent"] == None )
		assert ( r.joints[0]["channels"][0] == "xposition" )
		assert ( r.joints[0]["channels"][1] == "yposition" )
		assert ( r.joints[0]["channels"][2] == "zposition" )
		assert ( r.joints[0]["channels"][3] == "zrotation" )
		assert ( r.joints[0]["channels"][4] == "yrotation" )
		assert ( r.joints[0]["channels"][5] == "xrotation" )
		assert ( len ( r.joints[0]["children"] ) == 3 )

	def test_write ( self ) :
		# Arrange
		output_file_path = "$BVH_UTILS_PATH/tesset/output/t_pose.bvh"
		m = Manager (
			"$BVH_UTILS_PATH/tesset/input/t_pose.bvh",
			output_file_path
		)
		# Act
		m.load (  )
		m.write (  )
		# Assert
		with open ( os.path.expandvars ( output_file_path ) ) as output_file :
			assert ( len ( output_file.readlines (  ) ) == 101 )
