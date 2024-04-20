import unittest
from app.logstream.molecules.DateHeaderLog import DateHeaderLog
from app.logstream.Exceptions import LogstreamInputError, LogstreamReadError


class TestDateHeaderLogs(unittest.TestCase):

  def test_successful_fromInput(self):
    DateHeaderLog.fromInput('')
    DateHeaderLog.fromInput('1')
    DateHeaderLog.fromInput('+31')
    DateHeaderLog.fromInput('-31')
    DateHeaderLog.fromInput('365')

  def test_successful_fromSave(self):
    DateHeaderLog.fromSave('Saturday April 20, 2024')

  def test_failing_fromInput(self):
    self.assertRaises(LogstreamInputError, DateHeaderLog.fromInput, '=1')
    self.assertRaises(LogstreamInputError, DateHeaderLog.fromInput, 'one')
    self.assertRaises(LogstreamInputError, DateHeaderLog.fromInput, '-')

  def test_failing_fromSave(self):
    self.assertRaises(LogstreamReadError, DateHeaderLog.fromSave, 'April 20, 2024')
    self.assertRaises(LogstreamReadError, DateHeaderLog.fromSave, 'Sunday April 20, ')
    self.assertRaises(LogstreamReadError, DateHeaderLog.fromSave, '04/20/24')
    self.assertRaises(LogstreamReadError, DateHeaderLog.fromSave, 'Thursday February 29, 2023')
