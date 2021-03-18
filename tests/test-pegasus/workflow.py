#!/usr/bin/env python
import logging
from Pegasus.api import *

logging.basicConfig(level=logging.DEBUG)

tc = TransformationCatalog()
tc.add_transformations(
            Transformation(
                    "echo",
                    pfn="/usr/bin/echo",
                    site="condorpool",
                    is_stageable=False
                )
        )
tc.write()

wf = Workflow("test")
wf.add_jobs(Job("echo").add_args("hello world"))
wf.plan(submit=True).wait()
