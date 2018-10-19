import pandas as pd
import StringIO
import subprocess
import sys


JOB_NUMBER = sys.argv[1]
cmd = ['qacct', '-j', JOB_NUMBER]
p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
output = p.stdout.read()
a = pd.read_fwf(StringIO.StringIO(output),widths=[11,100], skiprows=[0], names=['attr', 'value'])
print(a.set_index('attr').to_json())

