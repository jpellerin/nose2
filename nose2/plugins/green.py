try:
    from gevent import monkey; monkey.patch_all()
    import gevent
except ImportError:
    gevent = None


import logging


from nose2 import events
from nose2.compat import unittest


log = logging.getLogger(__name__)



class GreenMP(events.Plugin):
    configSection = 'green'
    commandLineSwitch = ('G', '--green', 'Parallelize tests with gevent')

    def moduleLoadedSuite(self, event):
        event.suite.__class__ = GreenSuite


class GreenSuite(unittest.TestSuite):

    def run(self, result, debug=False):
        topLevel = False
        jobs = []
        if getattr(result, '_testRunEntered', False) is False:
            result._testRunEntered = topLevel = True

        for test in self:
            if result.shouldStop:
                break

            if _isnotsuite(test):
                self._tearDownPreviousClass(test, result)
                self._handleModuleFixture(test, result)
                self._handleClassSetUp(test, result)
                result._previousTestClass = test.__class__

                if (getattr(test.__class__, '_classSetupFailed', False) or
                    getattr(result, '_moduleSetUpFailed', False)):
                    continue

            if not debug:
                jobs.append(gevent.spawn(test, result))
            else:
                test.debug()

        if topLevel:
            self._tearDownPreviousClass(None, result)
            self._handleModuleTearDown(result)
            result._testRunEntered = False

        gevent.joinall(jobs, timeout=60)
        return result

# from unittest.suite
def _isnotsuite(test):
    "A crude way to tell apart testcases and suites with duck-typing"
    try:
        iter(test)
    except TypeError:
        return True
    return False
