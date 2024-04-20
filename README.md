# UT-Course-Availability-Tracker

This Python script, tailored specifically for the University of Texas at Austin, is currently undergoing early testing to streamline course enrollment processes. Designed to address the challenges of course waitlists, the script monitors the availability of courses and alerts users when a spot becomes open. Please note that this tool is in its early testing phase and is currently limited to UT Austin's course system.

In the dynamic academic environment of UT Austin, certain courses may lack a waitlist option, requiring vigilant monitoring to secure enrollment. This script automates the process, continuously checking for status changes and notifying users via text message when a coveted course becomes available. By leveraging this tool during its early testing phase, users can gain a competitive edge in course selection and enrollment.

# NOTE:
This script is in EARLY TESTING and ONLY WORKS IF DUO MOBILE IS SET TO CALL YOU! OTHERWISE it will NOT WORK! I am working to hopefully add functionality for mobile app users and text message users.

# Key Features:

- Specifically tailored for the UT course system.
- Allows you to 'snipe' non-waitlisted classes that randomly open and close.
- Customizable settings to meet individual preferences and needs.

### Usage:

To get started, first install the dependencies required for the script:
```python
pip install -r requirements.txt
```

Then, create a file titled "credentials.py" with the following format:
```python
USERNAME='your_UT_eid_here'
PASSWORD='your_password_here'
```

To run the script, simply navigate to the command line and run:
```python
python courseTrack.py -h
```