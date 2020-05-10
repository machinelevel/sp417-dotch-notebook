"""
This utility was bashed to gether by EJ in May 2020.
It's free for you to use in any way you see fit, and there's no warranty of any kind.
If you find it useful, please send me a note at notebook@machinelevel.com

Short joke: A termite walks into a bar and says "Hey where's the bar tender?"
"""


import moviepy.editor as mpy
from moviepy.video.fx.all import blackwhite, resize
import numpy as np

# rgb_to_hsv is super-handy, was written by Nikolay Polyarnyi
# Get it here: https://gist.github.com/PolarNick239/691387158ff1c41ad73c
from rgb_to_hsv_np import rgb_to_hsv

def mix_video_ink(t):
    """
    Insert ink from src to dest
    """
    src = ink_src
    dst = ink_dst
    vsrc = src['vid']
    vdst = dst['vid']
    fdst = vdst.get_frame(t) * (1.0 / 255.0)

    h_offset = 0
    if do_square:
        fw = fdst.shape[1]
        fh = fdst.shape[0]
        h_offset = (fw - fh) >> 1
        h_offset -= 100 # temp hack
        fdst = fdst[:,h_offset:h_offset+fh]

    if dst['t2'] is not None:
        total_time = dst['t2'] - dst['t1']
    if src['t2'] is not None:
        total_time = src['t2'] - src['t1']

    if t >= dst['t1'] and t <= dst['t1'] + total_time:
        if src['w'] != dst['w']:
            scale = float(dst['w'])/float(src['w'])
            vsrc = resize(vsrc, scale, 'bilinear')
        if do_monochrome_ink:
            vsrc = blackwhite(vsrc)
        fsrc = vsrc.get_frame(t + src['t1'] - dst['t1']) * (1.0 / 255.0)
        sx = int(scale*src['x'])
        sy = int(scale*src['y'])
        dx = int(dst['x'] - h_offset)
        dy = int(dst['y'])
        w = int(scale*src['w'])
        h = int(scale*src['h'])
#        fdst[dy:dy+h,dx:dx+w] = fsrc[sy:sy+h,sx:sx+w]

        fdst_hsv = rgb_to_hsv(fdst[dy:dy+h,dx:dx+w])
        saturation = fdst_hsv[:,:,1]
        hand = saturation > 0.25
        hand = hand.reshape((w * h))
        hand = np.dstack([hand, hand, hand])
        hand = hand.reshape((h, w, 3))

        inked = fdst[dy:dy+h,dx:dx+w] * fsrc[sy:sy+h,sx:sx+w]
        fdst[dy:dy+h,dx:dx+w] = hand * fdst[dy:dy+h,dx:dx+w] + (1 - hand) * fdst[dy:dy+h,dx:dx+w] * fsrc[sy:sy+h,sx:sx+w]

    return fdst * 255
    # print('dst',fdst[dy:dy+h,dx:dx+w].shape)
    # print('src',fsrc[sy:sy+h,sx:sx+w].shape)
    # print('scale',scale)
    # print('w',w)
    # print('h',h)
    # exit()
#    fdst[dy:dy+h,dx:dx+w] = fsrc[sy:sy+h,sx:sx+w]
#    return fdst * 255

do_square = True
do_monochrome_ink = False
video1 = mpy.VideoFileClip("./video/notebook-test-2.mp4")
video2 = mpy.VideoFileClip("./video/qcengine_test1.mov")
ink_dst = {'vid':video1, 't1':0.0, 't2':None, 'x':550, 'y':150, 'w':300, 'h':None}
ink_src = {'vid':video2, 't1':66.0, 't2':90.0, 'x':1185, 'y':520, 'w':740, 'h':400}

def do_add_ink():
    """
    Insert ink from src to dest
    """
    clip = mpy.VideoClip(mix_video_ink, duration=13.0)
    clip.write_videofile("test_edited.mp4", fps=24)

if __name__ == '__main__':
    do_add_ink()



