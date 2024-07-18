import random
import gradio as gr
from PIL import Image
import os
from fastapi import FastAPI
app = FastAPI()
CUSTOM_PATH = "/img"
def get_all_images():#本地圖片
    images = []
    directory = "./img/"
    for filename in os.listdir(directory):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            image = Image.open(directory+'/'+filename)
            images.append(image)
    return images

def fake_gan():
    images = get_all_images()
    selected_images = random.sample(images, 3)
    return selected_images

def create_gradio():
    # 使用 Blocks API 创建界面
    with gr.Blocks() as demo:
        gallery = gr.Gallery(
        label="Generated images", show_label=False, elem_id="gallery"
        , columns=[3], rows=[1], object_fit="contain", height="auto")
        btn = gr.Button("Generate images", scale=0)
        btn.click(fake_gan, None, gallery)
    return demo
gradio_app = gr.mount_gradio_app(app, create_gradio(), path=CUSTOM_PATH)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(gradio_app, port=8000)
