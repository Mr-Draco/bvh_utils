from hater import Manager

class Tester :
	def test_scale ( self ) :
		# Arrange
		output_file_path = "$BVH_UTILS_PATH/tesset/output/short_reference.bvh"
		m = Manager (
			"$BVH_UTILS_PATH/tesset/input/short_reference.bvh",
			output_file_path
		)
		# Act
		m.load (  )
		m.scale ( 1/100 )
		# Assert
		assert ( m.joints[1]['offset'][0] == 0.0157338 )
		assert ( m.joints[5]['offset'][1] == -0.0194743 )
		assert ( m.frames[0]['root']['position'][0] == 0.005909 )
		assert ( m.frames[1]['rwrist']['rotation'][0] == -19.6582 )

	def test_rotate ( self ) :
		# Arrange
		output_file_path = "$BVH_UTILS_PATH/tesset/output/short_reference.bvh"
		m = Manager (
			"$BVH_UTILS_PATH/tesset/input/short_reference.bvh",
			output_file_path
		)
		# Act
		m.load (  )
		m.rotate ( [ -90, 0, 0 ] )
		# Assert
		assert ( m.joints[1]['offset'][0] == 1.57338 )
		assert ( m.joints[5]['offset'][1] == -1.94743 )
		assert ( m.frames[0]['root']['position'][2] == -18.2650 )
		assert ( m.frames[1]['rwrist']['rotation'][0] == -19.6582 )
		m.write (  )
