# josa-model

Minimal utilities for choosing the correct Korean josa (조사) based on the
final sound of the preceding word.

## Example

```python
from josa_model import append_josa, pick_josa

pick_josa("사과", "은/는")   # "는"
pick_josa("집", "은/는")     # "은"
append_josa("길", "으로/로")  # "길로"
```