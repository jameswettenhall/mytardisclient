"""
Model class for MyTardis API v1's InstrumentResource.
"""
from __future__ import print_function

import json
import logging

import requests

from ..conf import config
from .facility import Facility
from .model import Model
from .resultset import ResultSet

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Instrument(Model):
    """
    Model class for MyTardis API v1's InstrumentResource.
    """
    def __init__(self, instrument_json):
        self.id = instrument_json['id']  # pylint: disable=invalid-name
        self.name = instrument_json['name']
        self.json = instrument_json
        self.facility = Facility(instrument_json['facility'])

    def __str__(self):
        """
        Return a string representation of an instrument
        """
        return "<%s: %s>" % (type(self).__name__, self.name)

    @staticmethod
    def list(facility_id=None, limit=None, offset=None, order_by=None):
        """
        Retrieve a list of instruments in a facility with ID facility_id.

        :param facility_id: The ID of a facility to retrieve instruments from.
        :param limit: Maximum number of results to return.
        :param offset: Skip this many records from the start of the result set.
        :param order_by: Order by this field.

        :return: A list of :class:`Instrument` records, encapsulated in a
            ResultSet object.
        """
        from ..utils import extend_url

        url = "%s/api/v1/instrument/?format=json" % config.url
        if facility_id:
            url += "&facility__id=%s" % facility_id
        url = extend_url(url, limit, offset, order_by)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        return ResultSet(Instrument, url, response.json())

    @staticmethod
    def get(**kwargs):
        r"""
        Retrieve a single instrument record

        :param \**kwargs:
          See below

        :Keyword Arguments:
            * *id* (``int``) --
              ID of the Instrument to retrieve

        :return: A :class:`Instrument` record.

        :raises requests.exceptions.HTTPError:
        """
        instrument_id = kwargs.get("id")
        if not instrument_id:
            raise NotImplementedError(
                "Only the id keyword argument is supported for Instrument get "
                "at this stage.")
        url = "%s/api/v1/instrument/%s/?format=json" % \
            (config.url, instrument_id)
        response = requests.get(url=url, headers=config.default_headers)
        response.raise_for_status()
        instrument_json = response.json()
        return Instrument(instrument_json=instrument_json)

    @staticmethod
    def create(facility_id, name):
        """
        Create an instrument record.

        :param facility_id: The ID of the facility to create the instrument in.
        :param name: The name of the instrument.

        :return: A new :class:`Instrument` record.
        """
        new_instrument_json = {
            "name": name,
            "facility": "/api/v1/facility/%s/" % facility_id
        }
        url = config.url + "/api/v1/instrument/"
        response = requests.post(headers=config.default_headers, url=url,
                                 data=json.dumps(new_instrument_json))
        response.raise_for_status()
        instrument_json = response.json()
        return Instrument(instrument_json)

    @staticmethod
    def update(instrument_id, name):
        """
        Update an instrument record.

        :param instrument_id: The ID of the instrument record to update.
        :param name: The new name of the instrument.

        :return: An updated :class:`Instrument` record.
        """
        updated_fields_json = {
            "name": name,
        }
        url = "%s/api/v1/instrument/%s/" % (config.url, instrument_id)
        response = requests.patch(headers=config.default_headers, url=url,
                                  data=json.dumps(updated_fields_json))
        response.raise_for_status()
        instrument_json = response.json()
        return Instrument(instrument_json)
