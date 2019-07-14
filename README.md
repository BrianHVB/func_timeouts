# func\_timeout
Python module to support running any existing function with a given timeout.


Function Timeout
================


func\_timeout
-------------

This is the function wherein you pass the timeout, the function you want to call, and any arguments, and it runs it for up to #timeout# seconds, and will return/raise anything the passed function would otherwise return or raise.

	def func_timeout(timeout, func, args=(), kwargs=None):
		'''
			func_timeout - Runs the given function for up to #timeout# seconds.

			Raises any exceptions #func# would raise, returns what #func# would return (unless timeout is exceeded), in which case it raises FunctionTimedOut

			@param timeout <float> - Maximum number of seconds to run #func# before terminating
			@param func <function> - The function to call
			@param args    <tuple> - Any ordered arguments to pass to the function
			@param kwargs  <dict/None> - Keyword arguments to pass to the function.

			@raises - FunctionTimedOut if #timeout# is exceeded, otherwise anything #func# could raise will be raised

			@return - The return value that #func# gives
		'''


**Example**


So, for esxample, if you have a function "doit('arg1', 'arg2')" that you want to limit to running for 5 seconds, with func\_timeout you can call it like this:


	from func_timeout import func_timeout, FunctionTimedOut

	...

	try:

		doitReturnValue = func_timeout(5, doit, args=('arg1', 'arg2'))

	except FunctionTimedOut:
		print ( "doit('arg1', 'arg2') could not complete within 5 seconds and was terminated.\n")
	except Exception as e:
		# Handle any exceptions that doit might raise here



func\_set\_timeout
------------------


This is a decorator you can use on functions to apply func\_timeout.

Takes two arguments, "timeout" and "allowOverride"

If "allowOverride" is present, an optional keyword argument is added to the wrapped function, 'forceTimeout'. When provided, this will override the timeout used on this function.


The "timeout" parameter can be either a number (for a fixed timeout), or a function/lambda. If a function/lambda is used, it will be passed the same arguments as the called function was passed. It should return a number which will be used as the timeout for that paticular run. For example, if you have a method that calculates data, you'll want a higher timeout for 1 million records than 50 records.


**Example:**

	@func_set_timeout(2.5)
	def myFunction(self, arg1, arg2):
		...

func timeout
------------------
This is another decorator you can use that will apply func\_timeout.
The decorator takes no parameters, but instead expects that the wrapped function will be called with an additional `timeout=` parameter. If no such parameter is passed to the decorated function, then it is invoked as if the decorator wasn't present.

**Example**

```python
@timeout()
def foo(arg1):
    #...
    pass
 
try:
    result = foo('bar', timeout=3)
except FunctionTimedOut:
    return None

```

FunctionTimedOut
----------------

Exception raised if the function times out.


Has a "retry" method which takes the following arguments:

	* No argument - Retry same args, same function, same timeout
	* Number argument - Retry same args, same function, provided timeout
	* None - Retry same args, same function, no timeout


How it works
------------

func\_timeout will run the specified function in a thread with the specified arguments until it returns, raises an exception, or the timeout is exceeded.
If there is a return or an exception raised, it will be returned/raised as normal.

If the timeout has exceeded, the "FunctionTimedOut" exception will be raised in the context of the function being called, as well as from the context of "func\_timeout". You should have your function catch the "FunctionTimedOut" exception and exit cleanly if possible. Every 2 seconds until your function is terminated, it will continue to raise FunctionTimedOut. The terminating of the timed-out function happens in the context of the thread and will not block main execution.


StoppableThread
===============

StoppableThread is a subclass of threading.Thread, which supports stopping the thread (supports both python2 and python3). It will work to stop even in C code.

The way it works is that you pass it an exception, and it raises it via the cpython api (So the next time a "python" function is called from C api, or the next line is processed in python code, the exception is raised).


Using StoppableThread
---------------------

You can use StoppableThread one of two ways:

**As a Parent Class**


Your thread can extend func\_timeout.StoppableThread\.StoppableThread and implement the "run" method, same as a normal thread.


	from func_timeout.StoppableThread import StoppableThread

	class MyThread(StoppableThread):

		def run(self):
			
			# Code here
			return


Then, you can create and start this thread like:

	myThread = MyThread()

	# Uncomment next line to start thread in "daemon mode" -- i.e. will terminate/join automatically upon main thread exit

	#myThread.daemon = True

	myThread.start()


Then, at any time during the thread's execution, you can call \.stop( StopExceptionType ) to stop it ( more in "Stopping a Thread" below

**Direct Thread To Execute A Function**

Alternatively, you can instantiate StoppableThread directly and pass the "target", "args", and "kwargs" arguments to the constructor

	myThread = StoppableThread( target=myFunction, args=('ordered', 'args', 'here'), kwargs={ 'keyword args' : 'here' } )

	# Uncomment next line to start thread in "daemon mode" -- i.e. will terminate/join automatically upon main thread exit

	#myThread.daemon = True

	myThread.start()


This will allow you to call functions in stoppable threads, for example handlers in an event loop, which can be stopped later via the \.stop() method.


Stopping a Thread
-----------------


The *StoppableThread* class (you must extend this for your thread) adds a function, *stop*, which can be called to stop the thread.


	def stop(self, exception, raiseEvery=2.0):
		'''
			Stops the thread by raising a given exception.

			@param exception <Exception type> - Exception to throw. Likely, you want to use something

			  that inherits from BaseException (so except Exception as e: continue; isn't a problem)

			  This should be a class/type, NOT an instance, i.e.  MyExceptionType   not  MyExceptionType()


			@param raiseEvery <float> Default 2.0 - We will keep raising this exception every #raiseEvery seconds,

				until the thread terminates.

				If your code traps a specific exception type, this will allow you #raiseEvery seconds to cleanup before exit.

				If you're calling third-party code you can't control, which catches BaseException, set this to a low number
				 
				  to break out of their exception handler.


			 @return <None>
		'''


The "exception" param must be a type, and it must be instantiable with no arguments (i.e. MyExceptionType() must create the object).

Consider using a custom exception type which extends BaseException, which you can then use to do basic cleanup ( flush any open files, etc. ).

The exception type you pass will be raised every #raiseEvery seconds in the context of that stoppable thread. You can tweak this value to give yourself more time for cleanups, or you can shrink it down to break out of empty exception handlers  ( try/except with bare except ).


**Notes on Exception Type**

It is recommended that you create an exception that extends BaseException instead of Exception, otherwise code like this will never stop:

	while True:
		try:
			doSomething()
		except Exception as e:
			continue

If you can't avoid such code (third-party lib?) you can set the "repeatEvery" to a very very low number (like .00001 ), so hopefully it will raise, go to the except clause, and then raise again before "continue" is hit.



You may want to consider using singleton types with fixed error messages, so that tracebacks, etc. log that the call timed out.

For example:

	class ServerShutdownExceptionType(BaseException):

		def __init__(self, *args, **kwargs):

			BaseException.__init__(self, 'Server is shutting down')


This will force 'Server is shutting down' as the message held by this exception.



Pydoc
=====

Find the latest pydoc at http://htmlpreview.github.io/?https://github.com/kata198/func_timeout/blob/master/doc/func_timeout.html?vers=4.3.3 .


Support
=======

I've tested func\_timeout with python 2.7, 3.4, 3.5, 3.6, 3.7. It should work on other versions as well.

Works on windows, linux/unix, cygwin, mac

ChangeLog can be found at https://raw.githubusercontent.com/kata198/func_timeout/master/ChangeLog 

Pydoc can be found at: http://htmlpreview.github.io/?https://github.com/kata198/func_timeout/blob/master/doc/func_timeout.html?vers=1
