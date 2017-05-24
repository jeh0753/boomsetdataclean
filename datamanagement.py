#import
import pandas as pd
import numpy as np
import csv

##import data
full = pd.read_csv('current_dataset.csv') # This is an export from the master file our organization keeps of all its members and their attendance histories
dirty = pd.read_csv('result.csv') # The data coming from boomset_merge.py
cp = pd.read_csv('cpfulllist.csv') # A direct export from campaignmonitor, all subscribers, name and email
## EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


# scrub emails
dirty['E-mail'] = dirty['E-mail'].str.strip().str.lower()
cp['E-mail'] = cp['Email Address'].str.strip().str.lower()
full['E-mail'] = full['E-mail'].str.strip().str.lower()


# scrub names(firstLAST) - note that for the cp dataframe, if last names are missing they fill in with middle initial or first name.
dirty['lastname'] = dirty['Last Name'].str.upper().str.strip()
dirty['fullname'] = dirty['First Name'].str.lower().str.strip() + dirty['lastname']
dirty['firstname'] = dirty['First Name'].str.lower().str.strip()
full['lastname'] = full['Last Name'].str.upper().str.strip()
full['fullname'] = full['First Name'].str.lower().str.strip() + full['lastname']
full['firstname'] = full['First Name'].str.lower().str.strip()
cp['lastname'] = cp['Name'].str.strip().str.rpartition(' ')[2].str.upper()
cp['fullname'] = cp['Name'].str.strip().str.partition(' ')[0].str.lower() + cp['Name'].str.strip().str.rpartition(' ')[2].str.upper()
cp['firstname'] = cp['Name'].str.strip().str.partition(' ')[0].str.lower()

# create a variable including the first letter of the first name lowercase, last name uppercase, and email address lowercase.
dirty['fLASTemail'] = dirty['fullname'].str[0] + dirty['lastname'] + dirty['E-mail']
full['fLASTemail'] = full['fullname'].str[0] + full['lastname'] + full['E-mail']
cp['fLASTemail'] = cp['fullname'].str[0] + cp['lastname'] + cp['E-mail']

# our unique identifiers for individuals are FIRSTNAMEemailaddress. Created here:
full['personkey'] = full['First Name'].str.upper().str.strip()
full['personkey'] += full['E-mail'].str.lower().str.strip()

# build a list of all individuals in our full dataframe, which counts attendance
persontable = full.groupby('personkey')
persontable = persontable.nth(0)

# separate out Campaign Monitor dataframe between those who are actively subscribed and those who are not (bounced emails, unsubscribed emails, etc.)
cp_good = cp.loc[cp['Status'] == 'Active']
cp_bad = cp.loc[cp['Status'] != 'Active']

## Create a list of elements of the new data where email is missing.
emiss = list(dirty[dirty['E-mail'] == '']['fullname'])
emisstable = dirty[dirty['E-mail'] == '']
emisstable.drop_duplicates(['fullname'])
emisstable.to_csv('emisstable.csv') #We export this to CSV so we have a list of email addresses that are missing.

# Create functions to look up emails, etc.
def emailfunc(df, emiss):
    ''' This function displays email addresses that are available in one of the 'good' dataframes (campaign monitor or the 'full' list, and 
        are missing from the dirty dataset'''
    result = []
    missing = []
    for i in emiss:
        if list(df[df['fullname'] == i]['E-mail']) != []:
            result.append((i, list(df[df['fullname'] == i]['E-mail'])[0:3]))
        else:
            missing.append(i)
    for x in result:
        print x[0], x[1]
    return missing

def emailfunc2(dirty, persontable, cp_good, newemail):
    ''' This function displays email addresses and names of individuals whose email addresses are available in one of the 'good' dataframes '''
    result = []
    missing = []
    for i in newemail:
        if list(dirty[dirty['E-mail'] == i]) != []:
            for y in list(dirty[dirty['E-mail'] == i]['fullname']):
                if not i == '':
                    result.append((y, i, str(list(persontable[persontable['fullname'] == y]['E-mail'])),str(list(cp_good[cp_good['fullname'] == y]['E-mail']))))
        else:
            missing.append(i)
    for x in list(set(result)):
        print x[0], x[1], x[2], x[3]
    return missing


def emailfunc2tocsv(df_dirty, df_clean, df_cp, elist): # these only exist as shortcut for manual pasting
    result = []
    missing = []
    for i in elist:
        if list(df_dirty[df_dirty['E-mail'] == i]) != []:
            for y in list(df_dirty[df_dirty['E-mail'] == i]['fullname']):
                if not i == '':
                    result.append((y, i, list(df_clean[df_clean['fullname'] == y]['E-mail']),list(df_cp[df_cp['fullname'] == y]['E-mail'])))
        else:
            missing.append(i)
    with open('resultstest.csv', 'wb') as csvfile:
        reswriter = csv.writer(csvfile, dialect='excel', delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for x in result:
            reswriter.writerow([x[0]] + [x[1]] + x[2] + x[3])

# Find available missing emails - fill these by hand, save result as cleaned.csv
emailfunc(cp_good, emiss) # use cp as a first source, full as secondary
emailfunc(full, emiss)


###Restart this document with cleaned.csv as dirty data

#### IMPROVEMENT: It would be great to map campaign monitor CSV data to the dirty missing email addresses.
#### still need to clean for non-email address data.

# Create a list of dirty data with emails that are not already on the list
newemail = list(set(dirty['E-mail'])-set(full['E-mail']))
bademail = list(cp_bad['E-mail'])
newemailnames = list(dirty[dirty['E-mail'].isin(newemail)]['fullname'])
newemail_bad = list(set(newemail)&set(bademail))
newemail_badnames = list(dirty[dirty['E-mail'].isin(newemail_bad)]['fullname'])
goodemail_badlist = list(set(full[full['fullname'].isin(newemail_badnames)]['E-mail']))

# Find new emails
emailfunc2(dirty, persontable, cp_good, newemail)

# Manually replace as needed - dirty.replace(whatitis, whatitshouldbe)
dirty = dirty.replace('dirtydataset_email','correct_email')

# check first names
dirty_n_full = dirty.append(persontable)

    for firstname, fLASTemail in dirty_n_full.groupby('fLASTemail'):
    thelist =[]
    thelist.append((firstname, fLASTemail))

# check duplicates

# export to CSV
dirty.to_csv('cleaned.csv')
