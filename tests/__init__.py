import unittest
import httpretty
import requests
import json
import os

from nose.tools import *
from nose.exc import SkipTest
from app.freebase import FreebaseClient