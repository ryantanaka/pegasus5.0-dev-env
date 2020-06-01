## Pegasus 5.0 Development Environment

Use this environment to play around with the 5.0 python api, develop and run
small workflows from a jupyter notebook or jupyter terminal. Nested docker 
containers are supported.

### Usage
1. `git clone https://github.com/ryantanaka/pegasus5.0-dev-env.git`
2. `./build.sh`
    - This will build the image from scratch and will take 10 minutes or so. 
    Subsequent calls to this always build from Pegasus master. All previous
    layers are cached and only Pegasus will be rebuilt. 
3. `./run.sh`
    - `./shared-data` will be bind mounted in the container to `/home/scitech/shared-data`
    - `jupyter notebook` will be running on `localhost:8888`
4. Go to `localhost:8888` and enter in the token provided from the terminal. 

For example, the output will look something like:

```
[I 16:41:49.373 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 16:41:49.377 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///home/scitech/.local/share/jupyter/runtime/nbserver-238-open.html
    Or copy and paste one of these URLs:
        http://cfc8f6cd945c:8888/?token=f0edbe8265f9b4745412e21350badc17cd729c0354e9e694
     or http://127.0.0.1:8888/?token=f0edbe8265f9b4745412e21350badc17cd729c0354e9e694
```

The token you would then use is: `f0edbe8265f9b4745412e21350badc17cd729c0354e9e694`

5. Once you've created a new jupyter notebook, create a block with `from Pegasus.api import *`,
    and run that block. At this point, the notebook will be set up with intellisense for the 5.0 python api. 
    Use `<TAB>` for code completion and `<SHIFT> + <TAB>` to bring up a function definition/docstring. 

You can also use the terminal provided by jupyter to directly interact with
the container. As such, you can run workflows from there as well. 
