# Cron Expression Parser

Cron expression parser is a simple command-line tool to parse cron expressions.

## Requirement
   - python 2.7

## How to run ?
   - python cron.py "*/15 0 1,15 * 1-5 /usr/bin/find"

## Supported Syntax
###  Format
   - "\<minute\> \<hour\> \<day of month\> \<month\> \<day of week\> \<command\>"
   - where minute , hours etc are tokens "command" is exception which is executable
   - each token can have following formats
        
        *  "*"     - wildcard all allowed values within the time value limits
        *  "*/5"   - values with regular step interval
        *  "5-7"   - range values
        *  "2,4,5" - specific values
        *  "5"     - single value
        

###  Sample Cron Expressions
```
     "*/15 0 1,15 * 1-5 /usr/bin/find"
     "* * * * * /usr/bin/find"
     "* */3 5 6 7 /usr/bin/find"
```
### Sample output of tool
     Input : "*/15 0 1,15 * 1-5 /usr/bin/find"
     Output :

            Minute        0 15 30 45
            Hour          0
            Day of Month  1 15
            Month         1 2 3 4 5 6 7 8 9 10 11 12
            Day of week   1 2 3 4 5
            Command       /usr/bin/find

## How to run unit test?
   - Go to the root folder of project and use following commands
       * python  -m unittest -v test_cron
       * python -m unittest  -v test_cron.TestCron.test_is_valid_number
