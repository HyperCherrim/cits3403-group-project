# cits3403-group-project

## Description

Our main purpose is for university students to create and join study groups.

We want to make it easier for you to find other students that are doing the same units as you at the same time, and help you find members for group projects (if your units have them).


Creators can plan the days and times they are available, add tags for which unit(s) they want to study.

Groups are available to join and their tags are automatically displayed on the home page.


This way every student can join groups that match the units they're currently studying.

Students can see when other students are avalible and plan meetings accordingly for study sessions.

## Group Details

| Student ID | Student Name     | GitHub Name     |
|------------|------------------|-----------------|
| 23724285   | Krish Dubey      | Krish-Dubey     |
| 23924286   | Atticus Bond     | HyperCherrim    |
| 23631345   | Callum Greenwald | CallumGreenwald |
| 23120741   | Nathan Foley     | Nathan-Foley    |

## Application Summary 

Utilising Flask, SQLAlchemy and Bootstrap to create a seamless and coherent study group experience.

## Launch Instructions: 
Before first launch, the database must be initialised to avoid errors.  To do this, enter the `Backend` directory and execute `flask db intit` then `flask db merge` then `flask db upgrade` to populate a new (empty) database file.  
After the database file has been created (check `app/` for a file named `appDatabase.db`), the app can be executed using `flask run`, also from the `Backend` folder.
### Note regarding launching from the ZIP file
- These instructions may differ based on how the submission is packaged - these instructions are for running the app from the Git repo.

## Running Tests

Currently no tests - these will be covered shortly.
