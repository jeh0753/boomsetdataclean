Cleaning Boomset Data Exports
=============================

Boomset (boomset.com) is a strong platform for tracking event attendance. But its inbuilt data analysis tools are weak, and you'll need to export your data to your own database in order understand retention of attendees between different events, general trends regarding attendance etc. This little applet takes Boomset attendee data from multiple events, compares it to your Campaign Monitor database (would require some editting to compare to MailChimp), and helps you merge clean data into your company's master database.


Running the Applet
------------------

To use this applet, you will first need to gather your data.

1. Get exports for all of the Boomset events you would like to import to your company database
2. Export your subscribers from Campaign Monitor
3. Add your Boomset file details to boomset_merge.py, using the instructions included in the file
4. Feed this, your Campaign Monitor data, and any pre-existing company attendee data into datamanagement.py.
5. Use the email 'replace' functionality to edit your database using the output you receive.


Helpful Resources
-----------------
For gaining familiarity with pandas and numpy, https://community.modeanalytics.com/python/ is a great resource.