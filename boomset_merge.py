import pandas as pd
import numpy as np

## Dates often come in incorrectly from Boomset. This function corrects it
def datecorrect(df, MM, DD, YYYY):
    df['Created'] = '{0}/{1}/{2} 15:46:39'.format(MM, DD, YYYY)
    df['Main Session Check-in Dates'] = '{0}/{1}/{2} 15:46:39'.format(MM, DD, YYYY)


## For each event you would like to import, create a dataframe in this format. Leave the Name, MM, DD, YYYY in quotes, but fill them with your data.
## Also update the file path.
df1 = pd.read_csv('boomset-export-filename.csv')
df1['Event Name'] = 'NAME'
datecorrect(df1, 'MM', 'DD', 'YYYY')

df2 = pd.read_csv('boomset-export-filename.csv')
df2['Event Name'] = 'NAME'
datecorrect(df2, 'MM', 'DD', 'YYYY')

# check that each dataframe has the same number of columns (sometimes Boomset changes its export files)
df1.shape, df2.shape

# merge data
frames = [df1, df2]
result = pd.concat(frames)

# Depending on how you run your event, it is likely no badges printed means the individual did not attend the event and can be omitted
result = result[result['Badges Printed'] != ' ']

# save back to csv
result.to_csv('result.csv')
