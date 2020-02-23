#!/bin/bash

. /Users/ehsan/miniconda2/etc/profile.d/conda.sh

conda activate tf

python incNET.py "$@"

