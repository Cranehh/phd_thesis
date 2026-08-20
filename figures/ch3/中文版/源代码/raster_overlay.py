# 位图贴中文：把原英文图渲染成高清位图，遮盖英文、叠加中文(宋体)。用于依赖模型数据、无法云端重画的图。
# spec 每项: (mx0,my0,mx1,my1, 文本, 字号(占图高比例), cx,cy, 旋转角, 对齐)  坐标均为0~1相对值
import subprocess, os
from PIL import Image, ImageDraw, ImageFont
R_DEFAULT="/tmp/fonts/NotoSerifSC-Regular.ttf"
def overlay(src_pdf, out_pdf, specs, dpi=220, font=R_DEFAULT):
    tmp=out_pdf+".src.png"
    subprocess.run(["pdftoppm","-png","-r",str(dpi),"-singlefile",src_pdf,tmp[:-4]],check=True)
    im=Image.open(tmp).convert("RGB"); W,H=im.size; d=ImageDraw.Draw(im)
    def F(px): return ImageFont.truetype(font,max(6,int(px)))
    for (mx0,my0,mx1,my1,text,sz,cx,cy,rot,al) in specs:
        if mx1>mx0 and my1>my0: d.rectangle([mx0*W,my0*H,mx1*W,my1*H],fill="white")
        px=sz*H
        if rot:
            t=Image.new("RGBA",(int(len(text)*px*1.15)+8,int(px*1.5)+8),(255,255,255,0))
            ImageDraw.Draw(t).text((t.size[0]/2,t.size[1]/2),text,font=F(px),fill="black",anchor="mm")
            t=t.rotate(rot,expand=True)
            im.paste(t,(int(cx*W-t.size[0]/2),int(cy*H-t.size[1]/2)),t)
        else:
            d.text((cx*W,cy*H),text,font=F(px),fill="black",anchor=al)
    os.remove(tmp); im.save(out_pdf,"PDF",resolution=float(dpi))
    print("saved",os.path.basename(out_pdf))
