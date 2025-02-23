from sqlalchemy import create_engine
from sqlalchemy import text

from tests.util import RPCTest


class PDNSTest(RPCTest):
    def cleanup_pdns_db(self, db_uri):
        with create_engine(db_uri).begin() as conn:
            conn.execute(text('delete from domains'))
            conn.execute(text('delete from domainmetadata'))
            conn.execute(text('delete from records'))

    def create_output_for_zone(self, zone, output, zone_group, db_uri):
        self.r.output_create(output, plugin='pdns-db', db_uri=db_uri)
        self.r.zone_group_create(zone_group)
        self.r.zone_group_add_zone(zone_group, zone)
        self.r.output_add_group(output, zone_group)
