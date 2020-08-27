# ActiveRoster2
A Python program for tracking attendence in virtual MS Teams meetings.  Unlike the original ActiveRoster which relied on Firebase, ActiveRoster2 uses the filesystem of your computer, ussually within a shared drive.  By using the filesystem and MS Teams exportand attednace sheets, ActiveRoster2 is far simpler and efficient than the original.  Where ActiveRoster was 1,442 lines of Python written over the course of a Summer, ActiveRoster2 is 124 lines (a 91% reduction) written all in one day. While that was fun to write, it often times pays to be efficient and focus on the core features users actually care about. This was written for HPRC to track attendence as meetings transitioned online due to COVID-19.

ActiveRoster2 checks the subdirectories of the directory it is in for MS Teams attendance files.  The attendance files MS Teams generates are tab separated value files although Microsoft mistakenly uses the ".csv" file type.  Each subdirectory is treated as a meeting category.  The attendace of every member that appears in any of the files is counted and a attendence ratio for every meeting type is calculated.  If they are active in at least two categories, they are listed as green to indicate they are an active member.

## Dependencies
ActiveRoster2 requires Python3.8 or greater.  You can download it from [python.org](https://www.python.org/downloads/) or the Windows Store.  It also requires that you use MS Teams for recording attendance.

## Use
### Taking Attendance
1. In an MS Teams meeting that you are hosting, go to the participants menu.
1. Click the three dots at the top of the menu and download the attendance sheet.
1. Find the file in your downloads folder and rename it to the date of your meeting.  If you have more than one in a day, add the time too.
1. Move the file to the subdirectory of the meeting type the meeting fits into.  ex: "Rocket Meetings"

### Viewing Attendance
To view your attendence, simply open ActiveRoster2 with Python.  All the members allong with a few statistics such as number of meetings and active members will be listed.  Green members are active while red members are inactive.  If you add or remove attendance files while the program is open, you can press "Recalculate" to find the new attendance statistics.
