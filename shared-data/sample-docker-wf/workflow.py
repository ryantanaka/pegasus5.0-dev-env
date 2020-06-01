#!/usr/bin/env python3
import os
import logging
import sys
import subprocess

from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)

# --- Import Pegasus API -------------------------------------------------------
from Pegasus.api import *

# --- Work Directory Setup -----------------------------------------------------
RUN_ID = "5.0.0dev-tutorial-wf-" + datetime.now().strftime("%s")
TOP_DIR = Path.cwd()
WORK_DIR = TOP_DIR / "work"

try:
    Path.mkdir(WORK_DIR)
except FileExistsError:
    pass

# --- Configuration (Pegasus Properties) ---------------------------------------
props = Properties()

props["pegasus.data.configuration"] = "nonsharedfs"


props["pegasus.monitord.encoding"] = "json"                                                                    
props["pegasus.catalog.workflow.amqp.url"] = "amqp://friend:donatedata@msgs.pegasus.isi.edu:5672/prod/workflows"

# pegasus-planner will, by default, pick up this file in cwd
props.write()

# --- Site Catalog -------------------------------------------------------------
# The Site Catalog describes the compute resources (which are often clusters) 
# that we intend to run the workflow upon. The SiteCatalog object and its usage
# resembles that of the pre 5.0.0dev XML site catalogs. If you have an existing
# XML site catalog, skip this step, and use pegasus-sc-converter to convert your
# catalog from XML to YAML.


sc = SiteCatalog()

shared_scratch_dir = str(WORK_DIR / RUN_ID)
local_storage_dir = str(WORK_DIR / "outputs" / RUN_ID)

local = Site("local")\
                .add_directories(
                    Directory(Directory.SHARED_SCRATCH, shared_scratch_dir)
                        .add_file_servers(FileServer("file://" + shared_scratch_dir, Operation.ALL)),
                    
                    Directory(Directory.LOCAL_STORAGE, local_storage_dir)
                        .add_file_servers(FileServer("file://" + local_storage_dir, Operation.ALL))
                )

condorpool = Site("condorpool")\
                .add_pegasus_profile(style="condor")\
                .add_pegasus_profile(auxillary_local="true")\
                .add_condor_profile(universe="vanilla")

sc.add_sites(local, condorpool)

# pegasus-planner will, by default, pick up this file in cwd
sc.write()

# --- Transformation Catalog (Executables and Containers) ----------------------
# In Pegasus lingo a transformation is the name for an executable, be it a 
# shell script, python script, or some compiled C code. We will catalog information
# about these transformations as well as the containers they use in the 
# TransformationCatalog object. 
tc = TransformationCatalog()

# Create and add our containers to the TransformationCatalog.

# A container that will be used to execute the following two transformations.
tools_container = Container(
                    "tools-container", 
                    Container.DOCKER, 
                    image="docker:///ryantanaka/preprocess:latest"
                )

tc.add_containers(tools_container)

# Create and add our transformations to the TransformationCatalog.

# An executable that is installed inside of "tools_container".
preprocess = Transformation(
                "preprocess",
                site="condorpool",
                pfn="/usr/local/bin/preprocess.sh",
                is_stageable=False,
                container=tools_container
            )

# A shell script that can be staged to some site and executed.
process_text = Transformation(
                    "process_text.sh", 
                    site="local", 
                    pfn=str(Path(__file__).parent.resolve() / "bin/process_text.sh"), 
                    is_stageable=True
                )

# A stageable python script that must be executed inside tools_container because
# it contains packages that we have when we develop locally, but may not be 
# installed on a compute node. 
process_text_2nd_pass = Transformation(
                            "process_text_2nd_pass.py",
                            site="workflow-cloud",
                            pfn="http://www.isi.edu/~tanaka/process_text_2nd_pass.py",
                            is_stageable=True,
                            container=tools_container
                        )

# An binary that is already installed on the condorpool site.
tar = Transformation(
        "tar",
        site="condorpool",
        pfn="/usr/bin/tar",
        is_stageable=False
    )

tc.add_transformations(preprocess, process_text, process_text_2nd_pass, tar)

# pegasus-planner will, by default, pick up this file in cwd
tc.write()

# --- Replica Catalog ----------------------------------------------------------
# Any initial input files must be specified in the ReplicaCatalog object. In this
# workflow, we have 1 input file to the workflow, and pegasus needs to know where
# this file is located. We specify that when calling add_replica().

initial_input_file = File("initial_input_file.txt").add_metadata(size=54)

rc = ReplicaCatalog()\
        .add_replica("local", "initial_input_file.txt", str(Path(__file__).parent.resolve() / "initial_input_file.txt"))\
        .write()

# Again, pegasus-planner will know to look for this file in cwd.

# --- Workflow -----------------------------------------------------------------
# Set infer_dependencies=True so that they are inferred based on job
# input and output file usage.
wf = Workflow("5.0.0dev-tutorial-wf", infer_dependencies=True)

# Create Jobs. These objects store just that. The transformation (executable)
# used by the job. The arguments passed to the executable. The input files used
# and the output files produced. 
preprocessed_data = File("preprocessed_data.txt")

job_preprocess = Job(preprocess)\
                    .add_args(initial_input_file, preprocessed_data)\
                    .add_inputs(initial_input_file)\
                    .add_outputs(preprocessed_data)

# Note that when passing File objects into add_args(), the file name is used.
# For example, add_args(initial_input_file, preprocessed_data) above is 
# the same as add_args(initial_input_file, "preprocessed_data.txt"). 

processed_data = File("processed_data.txt")

job_process_text = Job(process_text)\
                    .add_args(preprocessed_data, processed_data)\
                    .add_inputs(preprocessed_data)\
                    .add_outputs(processed_data)

twice_processed_data = File("twice_processed_data.txt")
extra_copy = File("backup.txt")

job_process_text_more = Job(process_text_2nd_pass)\
                            .add_args(processed_data, twice_processed_data, extra_copy)\
                            .add_inputs(processed_data)\
                            .add_outputs(twice_processed_data, extra_copy)

result = File("scientific_results.tar.gz")
compress = Job(tar, _id="tar_job")\
            .add_args("-cvzf", result, twice_processed_data, extra_copy)\
            .add_inputs(*job_process_text_more.get_outputs())\
            .add_outputs(result)

# With these jobs created, we can add them all to the workflow. The workflow
# object will automatically assign ids to the jobs (if none is given) and then
# determine the dependencies between them. 
wf.add_jobs(
    job_preprocess,
    job_process_text,
    job_process_text_more,
    compress
)

# Up until this point we have done the following:
# 1. Created a pegasus properties file. (Pegasus settings)
# 2. Created a site catalog. (Where will our workflow be executed?)
# 3. Created a transformation catalog. (What executables will our workflow use?)
# 4. Created a replica catalog. (Where are the initial input files used in this workflow located?)
# 5. Created jobs, which use transformations, and make up our workflow. (How are these executables used?)

# The next step is to run the workflow. This can be done through the wf object you
# created above. If you have used pegasus-plan before, usage will be almost identical.
try:
    wf.plan(
        dir=str(WORK_DIR),
        relative_dir=RUN_ID,
        submit=True
    ).wait()
except Exception as e:
    print(e.args[1].stdout)
    print(e.args[1].stderr)

