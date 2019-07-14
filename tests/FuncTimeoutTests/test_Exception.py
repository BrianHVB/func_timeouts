from func_timeout.exceptions import FunctionTimedOut


class TestException(object):

    def test_creating_timeout_exception_with_message_does_not_raise_error(self):
        ex = FunctionTimedOut("foo")

        try:
            raise ex
        except FunctionTimedOut as e:
            assert isinstance(e, FunctionTimedOut)

    def test_creating_timeout_exception_with_empty_message_does_not_raise_error(self):
        ex = FunctionTimedOut()

        try:
            raise ex
        except FunctionTimedOut as e:
            assert isinstance(e, FunctionTimedOut)

    def test_catching_general_exception_handles_function_timed_out_exception(self):

        def mocked_func():
            return True

        ex = FunctionTimedOut('This is a test', 1.5, mocked_func)

        try:
            raise ex
        except Exception as e:
            assert isinstance(e, FunctionTimedOut)
            assert issubclass(type(e), Exception)
