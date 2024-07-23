import subprocess
import shutil
import os

class HEVC:
    '''
        HEVC HM CODEC WRAPPER for creating the HDAC_HEVC training dataset
    '''
    def __init__(self,in_path,num_frames, bits=8, qp = 50,fps=30,frame_dim=(256,256),gop_size=10, config='source/hevc_hm/config_template.cfg', out_path="results"):
        self.qp = qp
        self.fps = fps
        self.bits= bits
        self.n_frames = num_frames
        self.frame_dim = frame_dim
        self.skip_frames = 0
        self.intra_period = -1

        self.seq_name = in_path.split("/")[-1].split(".")[0]
        self.out_path = f"{out_path}/{self.seq_name}_{qp}"
        self.config_name = 'hevc_'+str(qp)+'.cfg'
        self.config_path = config

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
        
        self.config_out_path = self.out_path+'/'+self.config_name
        self._create_config()

        #create yuv video
        self._mp4_2_yuv()

	
    def _create_config(self):
        '''
            Creates a configuration file for HEVC encoder
        '''
        with open(self.config_path, 'r') as file:
            template = file.read()
        #print(template)
        template = template.replace('inputYUV', str(self.in_yuv_path))
        template = template.replace('inputBit', str(self.bits))
        template = template.replace('outStream', str(self.ostream_path))
        template = template.replace('outYUV', str(self.dec_yuv_path))
        template = template.replace('inputW', str(self.frame_dim[0]))
        template = template.replace('inputH', str(self.frame_dim[1]))
        template = template.replace('inputNrFrames', str(self.n_frames))
        template = template.replace('intraPeriod', str(self.intra_period))
        template = template.replace('inputSkip', str(self.skip_frames))
        template = template.replace('inputFPS', str(self.fps))
        template = template.replace('setQP', str(self.qp))
        with open(self.config_out_path, 'w+') as cfg_file:
            cfg_file.write(template)

		
    def _mp4_2_yuv(self):
        #check for yuv video in target directory
        subprocess.call(['ffmpeg','-nostats','-loglevel','error','-i',self.in_mp4_path,self.in_yuv_path, '-r',str(self.fps)])


    def _yuv_2_mp4(self):
        cmd = ['ffmpeg','-nostats','-loglevel','error', '-f', 'rawvideo', '-pix_fmt','yuv420p','-s:v', f'{self.frame_dim[0]}x{self.frame_dim[1]}', '-r', str(self.fps), '-i', self.dec_yuv_path,  self.dec_mp4_path]
        subprocess.call(cmd)      
		
    def __str__(self) -> str:
        return "HEVC"
		
    def run(self):
        #Encoding
        cmd = ["source/hevc_hm/hm_16_15_regular/bin/TAppEncoderStatic", "-c", self.config_out_path,"-i", self.in_yuv_path]
        subprocess.call(cmd, stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
        
        #Decoding
        dec_cmd = ["source/hevc_hm/hm_16_15_regular/bin/TAppDecoderStatic", "-b", self.ostream_path,'-o',self.dec_yuv_path]
        subprocess.call(dec_cmd, stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
        self._yuv_2_mp4()
        shutil.rmtree(self.out_path)

				
