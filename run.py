import os
import imageio
from argparse import ArgumentParser
from source.hevc import HEVC
from source.vvenc import VvenC
from multiprocessing import Pool

CODECS = {'hevc': HEVC, 'vvc':VvenC}


def encode(params):
    coding_params = {'bits': 8, 
                     'qp': params[2],
                     'fps': params[3],
                     'frame_dim': params[4],
                     'gop_size': params[5], 
                     'out_path': params[6]}
    video = imageio.mimread(params[1], memtest=False)
    num_frames = len(video)
    codec = CODECS[params[0]](params[1],num_frames,**coding_params)
    codec.run()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--data",default='data/train',type=str, help="path to target videos stored in mp4 format")
    parser.add_argument("--codec", default='hevc',type=str, help="Encoding codec [hevc, vvc]")
    parser.add_argument("--qps",default="50,48,46,44", type=lambda x: list(map(int, x.split(','))),help="QP values for HEVC/VVC")
    parser.add_argument("--fps",default=25.0, type=float)
    parser.add_argument("--gop_size",default=-1, type=int)
    parser.add_argument("--out_path",default='data', type=str)
    parser.add_argument("--num_workers",default=5, type=int)
    opt = parser.parse_args()

    videos = os.listdir(opt.data)
    qps = opt.qps
    codec = opt.codec.lower()
    frame_dim = [256,256]

    params = [] 
    for vid in videos:
        for qp in qps:
            enc = [codec, f"{opt.data}/{vid}", qp, opt.fps, frame_dim, opt.gop_size, f"{opt.out_path}/{codec}_bl"]
            params.append(enc)
    # encode(params[0])
    pool = Pool(opt.num_workers)
    pool.map(encode, params[:10])