from common.utils import load_environment_variables

load_environment_variables (  )

from tesset.hater import _joints
t = _joints.Tester (  )
t.test_load (  )
t.test_write (  )

from tesset.hater import _frames
t = _frames.Tester (  )
t.test_load (  )
t.test_write (  )

from tesset.hater import Tester
t = Tester (  )
t.test_scale (  )
t.test_rotate (  )
