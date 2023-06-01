from typing import Iterable, Union
from boefjes.job_models import NormalizerMeta
from octopoes.models import OOI, Reference
from octopoes.models.ooi.dns.records import DNSPTRRecord
from octopoes.models.ooi.dns.zone import Hostname
from octopoes.models.ooi.network import IPAddress, Network
import ipaddress
import json

def run(normalizer_meta: NormalizerMeta, raw: Union[bytes, str]) -> Iterable[OOI]:
    address = normalizer_meta.raw_data.boefje_meta.input_ooi
    net = Reference.from_str(normalizer_meta.raw_data.boefje_meta.arguments["input"])
    results = json.loads(raw)
    for result in results:
        value = result["PTR"]
        # ip = result["IP"]
        network = Reference(Network(name=net))
        hostname = Hostname(name=value, network=network)
        ip_obj = ipaddress.ip_address(address)
        reversed_ip = ip_obj.reverse_pointer
        dnsptr_ooi = DNSPTRRecord(
            object_type="DNSPTRRecord",
            dns_record_type="PTR",
            value=value,
            hostname=Reference(hostname),
            address=Reference(address),
            reverse=reversed_ip
        )
        yield dnsptr_ooi
