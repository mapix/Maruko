# -*- coding: utf-8 -*-

from datetime import datetime
from collections import namedtuple

EPOCH = datetime.fromtimestamp(0)
GCM_API_KEY = 'AIzaSyCbYs51G44ZITEXz7GEUXtYDqASv1RZHLo'

MESSAGE_TYPE = namedtuple('MESSAGE_TYPE', ['STATISTIC', 'MESSAGE']
                          )('statistics', 'message')
TASK_ACTION = namedtuple('TASK_ACTION', ['PLAY', 'STOP']
                          )('play', 'stop')
MESSAGE_KIND = namedtuple('MESSAGE_KIND', ['WATERING', 'MESSAGE']
                          )('watering', 'message')
