import json
from typing import Iterable, Union

from boefjes.job_models import NormalizerMeta
from octopoes.models import OOI, Reference
from octopoes.models.ooi.dns.records import (
    DNSPTRRecord,
)


def run(normalizer_meta: NormalizerMeta, raw: Union[bytes, str]) -> Iterable[OOI]:
    address = Reference.from_str(normalizer_meta.raw_data.boefje_meta.input_ooi)
    results = json.loads(raw)
    for result in results:
        value = result["PTR"]
        network = result["ip"]
        dnsptr_ooi = DNSPTRRecord(value=value, pointer_hostname=Reference(Hostname(name=value)), ip_address=Reference(IPAddress(address=network)))
        yield dnsptr_ooi
