import cv2
import torch
import math
import numpy as np

def describe_opencv(model, img, kpts, N, mag_factor, use_gpu = False):
        """
        Rectifies patches around openCV keypoints, and returns patches tensor
        """
        patches = []
        for kp in kpts:
            x,y = kp.pt
            s = kp.size
            a = kp.angle

            s = mag_factor * s / N
            cos = math.cos(a * math.pi / 180.0)
            sin = math.sin(a * math.pi / 180.0)

            M = np.matrix([
                [+s * cos, -s * sin, (-s * cos + s * sin) * N / 2.0 + x],
                [+s * sin, +s * cos, (-s * sin - s * cos) * N / 2.0 + y]])

            patch = cv2.warpAffine(img, M, (N, N),
                                 flags=cv2.WARP_INVERSE_MAP + \
                                 cv2.INTER_CUBIC + cv2.WARP_FILL_OUTLIERS)

            patches.append(patch)
#         print("BeepBooop")
        patches = torch.from_numpy(np.asarray(patches)).float()
        patches = torch.unsqueeze(patches,1)
#         print("BeepBooop2")
        
        if use_gpu:
#             print("BeepBooop-GPU")
            patches = patches.cuda()
#             print("BeepBooob3")
        descrs = model(patches)
#         print("BeepBooop4")
        return descrs.detach().cpu().numpy()
        
