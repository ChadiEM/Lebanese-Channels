#!/bin/bash

docker build -t lebanese_channels . && docker run -p 12589:12589 -it lebanese_channels