import qutip as qp
import numpy as np 
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation, FFMpegWriter
from PIL import Image


def cartoon(x,y,z,name):
    image_list = []
    for i in range(len(x)):
        def trace(t):
            if t==0:
                pass
            else:
                b.add_points([x[:t], y[:t], z[:t]])
        b = qp.Bloch()
        trace(i)
        vec = [x[i], y[i], z[i]]
        b.add_vectors(vec)
        b.render()
        image_list.append(b.fig)

    def figure_to_array(fig):
        # 渲染 Figure 对象为 RGBA 图像数据
        fig.canvas.draw()
        buf = fig.canvas.tostring_rgb()
        ncols, nrows = fig.canvas.get_width_height()

        # 将 RGBA 数据转换为 numpy 数组
        img = np.frombuffer(buf, dtype=np.uint8).reshape(nrows, ncols, 3)
        return img

    def update(frame):
        plt.clf()  

        fig = image_list[frame]
        # 将 Figure 对象转换为 numpy 数组
        img_array = figure_to_array(fig)
        # 显示图像
        plt.imshow(img_array)
        plt.title(f'Frame {frame}')
        plt.axis('off')  # 关闭坐标轴显示，如果不需要

    # 创建动画对象
    fig, ax = plt.subplots()
    ani = FuncAnimation(fig, update, frames=len(image_list), interval=100)

    # 保存动画为视频文件（MP4 格式）
    writer = FFMpegWriter(fps=5)  # 设置帧率（每秒帧数）
    ani.save(f'{name}.mp4', writer=writer)

    plt.show()






























