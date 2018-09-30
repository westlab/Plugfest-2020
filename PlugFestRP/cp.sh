#!/bin/sh
scp -r "pi@10.1.1.50:/export/{alps,bluetooth-com,mqtt-client-py,TEDS}" .
scp -r "pi@10.1.1.51:/export/{alps,bluetooth-com,mqtt-client-py,TEDS}" .
