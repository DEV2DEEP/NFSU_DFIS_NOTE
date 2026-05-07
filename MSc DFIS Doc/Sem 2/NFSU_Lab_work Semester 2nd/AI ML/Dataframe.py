

import pandas as pd 
import numpy as np 

p = {'Name':['Akash','Gopal','Yash','Zeel',np.nan],'Age':[21,23,20,54,34],
'Job':['Engineer','Teacher','Scientist','Businessman','Mafia']}
a = pd.DataFrame(p)
b = pd.isnull(p)
print(a)
print( b)
