# Description
A graphical interface serial communication program with combination of command function. [一个带有组合命令功能的的图形界面串口通讯程序。]

![gpserial main frame screenshot](gpserial-main.png)
![gpserial add dialog screenshot](gpserial-add.png)

# Paremeter note
* Direct

    Table: code
    
    code        compute value           pratical value
    --------    ---------------         ----------------
    a1          0--F(0--15)             0, F(0, 15)
    a2          0--F(0--15)             min_time--F(min_time--15)
    a3          00-FF(00--FF)           00--FF(0--255)
    a4          0000-FFFF(0--65535)     min_time2--FFFF(min_time2--65535)
    a5          00--FF(0--255)          01-FF(1--255)
    
    
    Table: parameter
    
    parameter       compute eauation    value
    --------------  -----------------   ------
    direct          0->0, F->1          0, 1
    speed           a2 * 5              (min_time * 5)--75
    step_distance   a3 * motor_step     0--(255 * motor_step)
    pause_time      a4                  min_time2--65535
    count           a5                  1-255


When distance is big than max step_distance in single cycle, we must do action
more than one.

One method is divide the convered distance in two interger number for
step_distance and cycle times, the numbers is called factor. we also need to
filter the factor so that they fit two variables' limit.  I come out a idea:
divide the converted distance in two number, which their muliplity is mostly
near the distance, then get max factor up to single cycle for that variable,
the other one for cycle time. but we faced a problem that how to get the two
numbers.

The other one method is divide the converted distance, getting the times and
left number. we use max variable value for single cycle, and the times number
for count time to do one cycle action, then use the left number for variable
value fro single cycle, and one for count time to complete another cycle action.
That is to say, we must do two action.

I think the later method is easier and clear than former.

Time is dealed with same method.

# Develop environment
* Python 2.7.9
* pyserial 3.2.1
* wxPython 3.0.1.1
