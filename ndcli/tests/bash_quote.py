import subprocess
import shlex

import hypothesis.strategies as st
from hypothesis import given, settings, assume


@given(st.text(alphabet=''.join(chr(a) for a in range(1, 128))))
@settings(max_examples=50000)
def test(s):
    assume(not s.startswith('-'))
    s = str(s)
    quoted = shlex.quote(s)
    command = 'echo -n ' + quoted
    out = subprocess.check_output(['bash', '-c', command], shell=False, text=True)
    assert out == s

