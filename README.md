# SSHHoneypot
A simple ssh honeypot written in Python.

# Installation

Note: The following steps pertain to installation on a Linux/Unix machine. It also requires Python 3.5+.

1. Clone the repository on your local machine
`git clone https://github.com/DeveshChande/SSHHoneypot`

2. Create a virtual environment.
`virtualenv venv`


3. Activate the virtual environment.
`source venv/bin/activate`

4. Create a empty folder named 'sshlogs'.
`mkdir sshlogs`

5. Run main.py with the appropriate option. (--password for using password authentication and --key for using public key authentication)

    `python main.py [--password]/[--key]`

6. Set a termination timeout according to your need by modifiying the value of `(t1-t0) >` in *both* `PasswordServer` and `PublicKeyServer` classes.

7. After termination of `main.py`, run `python log-parser.py` to parse generated log file. This will create *additional* log files in `sshlogs` directory.
