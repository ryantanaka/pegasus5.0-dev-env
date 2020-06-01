This tutorial uses the latest 5.0.0dev version of Pegasus. First you will need to follow the [Building from Source Instructions](https://github.com/pegasus-isi/pegasus).

1. Install source dependencies 
2. `git clone https://github.com/pegasus-isi/pegasus.git`
3. In the `pegasus` directory, run `ant dist`. Note that if you don't have R installed, before running `ant dist`, run `export PEGASUS_BUILD_R_MODULES=0`. 
4. Add binaries to your `PATH`: `export PATH=<path to cloned repo>/pegasus/dist/pegasus-5.0.0dev/bin:$PATH`
5. Running `pegasus-version` should display `5.0.0dev` 

For documentation and usage examples of the python api, see
[Pegasus 5.0 Python API Docs](https://pegasus.isi.edu/docs/5.0.0dev/python/Pegasus.api.html#module-Pegasus.api)
