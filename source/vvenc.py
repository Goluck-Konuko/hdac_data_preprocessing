import subprocess
import imageio
import shutil
import os


class VvenC:
    '''
        VvenC CODEC WRAPPER
    '''
    def __init__(self,in_path,num_frames, bits=8, qp = 50,fps=30,frame_dim=(256,256), out_path="results", **kwargs):
        self.qp = qp
        self.fps = fps
        self.bits= bits
        self.n_frames = num_frames
        self.frame_dim = f"{frame_dim[0]}x{frame_dim[1]}"
        self.skip_frames = 0
        self.intra_period = -1

        self.seq_name = in_path.split("/")[-1].split(".")[0]
        self.out_path = f"{out_path}/{self.seq_name}_{qp}"

        #inputs
        self.in_mp4_path = in_path
        self.in_yuv_path = self.out_path+'/in_video_'+str(self.qp)+'.yuv'

        #outputs
        self.ostream_path = self.out_path+'/out_'+str(self.qp)+'.bin'
        self.dec_yuv_path = self.out_path+'/out_'+str(self.qp)+'.yuv'
        self.dec_mp4_path = f"{out_path}/{self.qp}/{self.seq_name}.mp4" #self.out_path+'/out_'+str(self.qp)+'.mp4'
        os.makedirs(f"{out_path}/{self.qp}/", exist_ok=True)
        #logging file
        self.log_path =  self.out_path+'/out_'+str(self.qp)+'.log'
        os.makedirs(self.out_path, exist_ok=True)
        
        #create yuv video
        self._mp4_2_yuv()

    def _yuv_2_mp4(self):
        cmd = ['ffmpeg','-nostats','-loglevel','error', '-f', 'rawvideo', '-pix_fmt','yuv420p10le','-s:v', self.frame_dim, '-r', str(self.fps), '-i', self.dec_yuv_path,  self.dec_mp4_path]
        subprocess.call(cmd)
	
    def _mp4_2_yuv(self):
        #check for yuv video in target directory
        subprocess.call(['ffmpeg','-nostats','-loglevel','error','-i',self.in_mp4_path,self.in_yuv_path, '-r',str(self.fps)])


    def _get_decoded_frames(self):
        #convert yuv to mp4
        
        frames = imageio.mimread(self.dec_mp4_path, memtest=False)
        # hevc_frames = torch.tensor(np.array([np.array([img_as_float32(frame) for frame in frames]).transpose((3, 0, 1, 2))]), dtype=torch.float32)
        return frames

		
    def run(self):
        ## Encoding
        cmd = ['vvencapp', '--preset', 'fast', '-i', self.in_yuv_path, '-s', self.frame_dim,'-q', str(self.qp),   '-f', str(self.n_frames),'-ip',str(self.intra_period), '-o', self.ostream_path]
        subprocess.call(cmd, stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
 
        dec_cmd = ['vvdecapp', '-b', self.ostream_path, '-o', self.dec_yuv_path]
        subprocess.call(dec_cmd, stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
        self._yuv_2_mp4()

        shutil.rmtree(self.out_path)
