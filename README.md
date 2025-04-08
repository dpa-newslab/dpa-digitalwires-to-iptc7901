# dpa-digitalwires-to-iptc7901

This project provides a method for transforming entries from the dpa-digitalwires format into an
approximate [IPTC 7901](http://www.iptc.org/std/IPTC7901/1.0/specification/7901V5.pdf) article format. We tried to
closely emulating the IPTC standard while acknowledging inherent limitations.

This converter creates an **approximation** of the IPTC 7901 format because some information needed for a precise
transformation may not be available in the dpa-digitalwires source data. Despite these limitations, the tool provides a
practical solution for enhancing interoperability and workflow efficiency.

## Getting started

```
pipenv install "git+https://github.com/dpa-newslab/dpa-digitalwires-to-iptc7901.git
```

This setup was tested with:

* =Python3.12

Install requirements by calling:

```
pip install -r requirements.txt
```

```python
import iptc7901
import json

with open("path/to/digitalwires.json") as f:
    dw = json.load(f)
    iptc_messages = iptc7901.convert_to_iptc(dw)
```

The function returns a list of IPTC message for each service specified in the digitalwires message, denoted by
`"type": "dnltype:wire"`. If there is no such entry in the digitalwires message, no IPTC message is generated.
Otherwise, if the digitalwires contains for example the service `dpasrv:bdt` and `dpasrv:eca` the function will return
similar IPTC message. They only differ in their IPTC Headers.

The header has the following structure:

```
<DNST><DLFD> <PRIO> <RESS> <WANZ>  <AGNT> <ALFD>  <BEZU>
```

For more information on these fields, please refer
to [this documentation](https://a.storyblok.com/f/166218/x/a2b4b08be2/supportseite_iptc7901_textformat.pdf).

**Note**:

- `DNST` is the abbreviation of the service mapped by `iptc7901.utils.Mappings.service_mnemonic_map`
- `AGNT` will be mapped from the service by `iptc7901.utils.Mappings.service_to_iptc_agency_map`.

Both `DLFD` and `ALFD` are sequence numbers that are hard-coded to `0000` if both generators are not provided. When you
use the parameters `service_sequence_generator` and `agency_sequence_generator`, both will be applied to each service.
This means that if the message includes two services, both generators will be called twice, sending the service
abbreviation or agency to them, respectively. This allows the generators to yield different values for different
services or agencies.

An example of a generator might look like this:

```python
import iptc7901
import json
from collections import defaultdict
from itertools import count

_sequences = defaultdict(count)

def find_sequence(key):
    return _sequences[key]

with open("path/to/digitalwires.json") as f:
    dw = json.load(f)
    iptc_messages = iptc7901.convert_to_iptc(dw, find_sequence)
```

However, it is up to the generator to persist the current state between each call of `convert_to_iptc()`.

## Tests

```
pip install -r requirements-test.txt
pytest -s tests
```

## License

Copyright 2025 dpa-IT Services GmbH

Apache License, Version 2.0 - see `LICENSE` for details.