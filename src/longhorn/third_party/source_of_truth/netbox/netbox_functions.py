"""
Contains all the functions needed for the netbox blueprint.
Things such as routes and forms should be in separate files.
"""
from flask import current_app as app
from pynetbox import api
import requests.exceptions


class Netbox:
    # pylint: disable=too-few-public-methods
    """
    Builds an object that interacts with Netbox API.

    `circuit` object contains the following data:

        - id
        - url
        - display
        - cid
        - provider (dict)
            - id
            - url
            - display
            - name
            - slug
        - type (dict)
            - id
            - url
            - display
            - name
            - slug
        - status (dict)
            - value
            - label
        - tenant
        - install_date
        - commit_rate
        - description
        - termination_a (dict)
            - id
            - url
            - display
            - site (dict)
                - id
                - url
                - display
                - name
                - slug
            - provider_network
            - port_speed
            - upstream_speed
            - x_connect_id
        - termination_z (dict)
            - id
            - url
            - display
            - site (dict)
                - id
                - url
                - display
                - name
                - slug
            - provider_network
            - port_speed
            - upstream_speed
            - x_connect_id
        - comments
        - tags (list)(dict)
            - id
            - url
            - display
            - name
            - slug
            - color
        - custom_fields (dict)
        - created
        - last_updated

    `provider` object contains the following data:

        - id
        - url
        - display
        - name
        - slug
        - asn
        - account
        - portal_url
        - noc_contact
        - admin_content
        - comments
        - tags (list)
        - custom_fields (dict)
        - created
        - last_updated
        - circuit_count

    `site_a` and `site_z` objects contains the following data:

        - id
        - url
        - display
        - name
        - slug
        - status (dict)
            - value
            - label
        - region (dict)
            - id
            - url
            - display
            - name
            - slug
            - _depth
        - group
        - tenant
        - facility
        - asn
        - asns (list)
        - time_zone
        - description
        - physical_address
        - shipping_address
        - latitude
        - longitude
        - contact_name
        - contact_phone
        - contact_email
        - comments
        - tags (list) (dict)
            - id
            - url
            - display
            - name
            - slug
            - color
        - custom_fields (dict)
        - created
        - last_updated
        - circuit_count
        - device_count
        - prefix_count
        - rack_count
        - virtualmachine_count
        - vlan_count
    """

    def __init__(self, side_a: str, side_z: str):
        try:
            self.api = api(url=app.config["NETBOX_URL"], token=app.config["NETBOX_TOKEN"])
            self.circuit = self.api.circuits.circuits.get(
                cid=self.api.circuits.circuits.filter(tag=[side_a.lower(), side_z.lower()])
            )
            self.provider = self.api.circuits.providers.get(self.circuit.provider.id)
            self.site_a = self.api.dcim.sites.get(self.circuit.termination_a.site.id)
            self.site_z = self.api.dcim.sites.get(self.circuit.termination_z.site.id)
            self.journal_entries = self.api.extras.journal_entries.filter(
                assigned_object_type="circuits.circuit",
                assigned_object_id=self.circuit.id
            )
        except requests.exceptions.ConnectionError:
            pass

    def check_journal_entries(self):
        """
        Loops through journal entries and extracts strings that reflect ticket numbers
        """
        incidents = []
        for entry in self.journal_entries:
            if "Incident opened" in entry.comments:
                incidents.append(str(entry.comments).split()[-1])
        app.logger.info(f"Found incidents: {incidents}")
        return incidents
