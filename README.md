# DATA PREPROCESSING FOR HDAC (+) TRAINING
HDAC models require base layer frames to animate target frames with higher semantic and pixel fidelity.
This repository provides the scripts for creating the dataset used for training HDAC and its extensions used in the JVET-AH0114 standardization.
## Dependencies
1. HEVC_HM Codec : A compiled binary of HEVC_HM_16_15 is provided with this repository. [OPTIONAL] - Compile a later version if necessary.
2. VVenC: Find the compile and install directions from https://github.com/fraunhoferhhi/vvenc

NOTE: We use VVenC as the representative VVC codec to allow for reasonable processing time for large datasets

STEP 1: CREATE A Talking-Head dataset such as VoxCeleb e.g (https://github.com/AliaksandrSiarohin/video-preprocessing)

STEP 2: Create HEVC / VVC encodings with multiple quality levels by running:
`python run.py --data PATH_TO_DATASET --codec CODEC_NAME --qps COMMA_SEPARATED_QP_LIST `
