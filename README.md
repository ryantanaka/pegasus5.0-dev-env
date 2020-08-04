## Pegasus 5.0 Development Environment

Use this environment to play around with the 5.0 python api, develop and run
small workflows from a jupyter notebook or jupyter terminal. Nested docker 
containers are supported.

### Usage
1. `git clone https://github.com/ryantanaka/pegasus5.0-dev-env.git`
2. `./build.sh`
    - This will build the image from scratch and will take 10 minutes or so. 
    Subsequent calls to this always build the latest Pegasus master. All previous
    layers are reused and only Pegasus will be rebuilt. 
3. `./run.sh`
    - `./shared-data` will be bind mounted in the container to `/home/scitech/shared-data`
    - `jupyter notebook` will be running on `localhost:8888`
4. Go to `localhost:8888` and enter `scitech` as the password. 

For example, the output will look something like:

5. Once you've created a new jupyter notebook, create a block with `from Pegasus.api import *`,
    and run that block. At this point, the notebook will be set up with intellisense for the 5.0 python api. 
    Use `<TAB>` for code completion and `<SHIFT> + <TAB>` to bring up a function definition/docstring. 

You can also use the terminal provided by jupyter to directly interact with
the container. As such, you can run workflows from there as well. 
