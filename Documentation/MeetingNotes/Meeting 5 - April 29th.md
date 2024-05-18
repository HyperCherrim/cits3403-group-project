(finally get things going at 3:20pm)

## Last Time:
- Table thing (time/date selector) should now be working correctly

- Nathan still stuck in Operation Timetable
- <span style=color:yellow>Self</span> - trying (and failing) to set up the DB
- Callum: Write the Python code to check for valid times
	- Mixed success - will continue/finish this week
- Krish - job got stolen (whoops - my bad...)


## TODO:
KEY: `*` - come back to later
- User page`*`/Group Page?
	- Having it show notifications
	-  Should be limited to valid groups?
- Bootstrap! (On *all* pages)
	- General styling
- No email
- 404 page? (not really)
- Dark Mode (extra?)
- Testing
- Citations
- Rearranging the repository
- About Me? (So what is it? - Danny John-Jules)


- Unfortunately we don't have any biscuits, but maybe next time?


## Who's doing what this week?
- Nathan:  Continue imprisonment in Operation TimeTable
- Callum: The (watchamacallit) User page
- Myself (Atticus): Database (continuing)
- Krish: Bootstrap
	- If Bootstrap is finished early, Callum will steal Krish to work on the User page

*some pirate talk*


## User Page
- Navbar!
- Simple design - 
- Link to change Pwd
- (Gin)Jin(ger)ja link
- Email
- List group membership?

- Flash notification with group details?
- Remove user from groups once they are finished (or on user request?)

- Notifications on group formation
	- Notifications table
	- Group and User as FKs, Seen as a boolean (sortable)
	- When they log in, run a SQL query to populate the page with notifications
	- Matches username when loading
	- Change value from "non-red" to red?

or
- Login
- Have a thing that queries for any unread notifications belonging to the user, then show them 
- Change the menu bar to show the logged-in user


- Needed: Link to group, 

- Every time the DB is modified, a function will have to be called 
	- Function processes times as strings, makes them to a list and returns available times

- Squircles with names, times being selected, user emails
- Change p/w, list email, active groups (Title or Title/Description depending on group decisions)
	- Notifications
	- Only notify the relevant people (who specify that the time actually works)
		- Additional notification specifying a change of time?