## Pegasus 5.0 Development Environment

Use this environment to play around with the 5.0 python api, develop and run
small workflows from a jupyter notebook or jupyter terminal. Nested docker 
containers are supported.

cuda10.1 and cudnn7.0 are also installed. To use this, your host machine must have
the [Nvidia Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/overview.html) 
installed and an nvidia gpu with cuda10.1+ installed. 

Note that when using nested Docker containers, the nested container will not have access to the host 
GPU. GPU support is only provided through this development container, and will not be provided from
within containers nested in this one. 

### Usage
1. `git clone https://github.com/ryantanaka/pegasus5.0-dev-env.git`
2. `cd pegasus5.0-dev-env`
3. `mkdir -p ./shared-data && sudo chown :808 ./shared-data && chmod 775 ./shared-data && chmod g+s ./shared-data`
4. If do not have the required GPU resources mentioned above, [uncomment line 4, and comment line 5 in run.sh](https://github.com/ryantanaka/pegasus5.0-dev-env/blob/0dbf8a5df8966b7e250c34f60ef814cc8a4578c1/run.sh#L4-L5). 
5. `./run.sh`
    - `./shared-data` will be bind mounted in the container to `/home/scitech/shared-data`
    - `jupyter notebook` will be running on `localhost:8888`
6. Go to `localhost:8888` and enter `scitech` as the password. 

For example, the output will look something like:

7. Once you've created a new jupyter notebook, create a block with `from Pegasus.api import *`,
    and run that block. At this point, the notebook will be set up with intellisense for the 5.0 python api. 
    Use `<TAB>` for code completion and `<SHIFT> + <TAB>` to bring up a function definition/docstring. 

You can also use the terminal provided by jupyter to directly interact with
the container. As such, you can run workflows from there as well. 
