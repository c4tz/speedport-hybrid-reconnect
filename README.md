# speedport-hybrid-reconnect
Reconnect your Speedport Hybrid easily by using this class.

## Usage:

```python
from router import SpeedportHybrid

router = SpeedportHybrid('ROUTERPASSWORD')
router.reconnect()
```

You can now also get all devices in you LAN with:

```python
router.getDevices()
```

returns:

```python
['Device#1 (192.168.1.100)', "Device#2 (192.168.1.101)", ...]
```
